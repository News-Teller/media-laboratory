import os
import sys
import logging
from datetime import datetime
import re
from typing import Optional
from typing import List
import pymongo
from pymongo.errors import ConnectionFailure, PyMongoError
import dash

from .serializer import dashapp_serializer, dashapp_deserializer

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
logger.setLevel(os.getenv('LOG_LEVEL', 'WARNING').upper())


# regex for a valid uid
UID_PATTERN = re.compile('^[a-zA-Z0-9_-]+$')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

class DataVizException(Exception):
    pass

class DataViz(metaclass=Singleton):
    """
    Access DataViz functionalities via this interface.

    :raises:
        ValueError: If there's an error during the initialisation/configuration.
    """
    _db_name = os.getenv('DB_NAME', 'medialab')
    _collection_name = os.getenv('DB_COL_NAME', 'viz')


    def __init__(self, uri: Optional[str] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'), user: Optional[str] = os.getenv('DB_USER')):
        self._client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        self._db = self._client[self._db_name]
        self._collection = self._db[self._collection_name]
        self.user = user

        # If the user is not provided as parameter or with a dedicated env var,
        # try use the JupyterHub user
        if not self.user:
            if os.getenv('JUPYTERHUB_USER'):
                self.user = os.getenv('JUPYTERHUB_USER')
            else:
                raise ValueError('User not provided!')

    def store(self,
        uid: str,
        title: str,
        dash_app: dash.Dash,
        tags: List[str] = [],
        locked: bool = False
        ) -> bool:
        """Store a visualisation onto the database.

        :param uid: Visualisation unique identifier (must match '^[a-zA-Z0-9_-]+$')
        :type uid: str
        :param title: A title, more human readable than the `uid`.
            Can be different from the Dash app title.
        :type title: str
        :param app: Dash applicatiomn
        :type app: `dash.Dash`
        :param tags: List of tags (words) to ease the retrieval.
        :type tags: List[str]
        :param locked: Set to `True` to lock this visualisation, defaults to False
        :type locked: bool, optional
        :raises
            ValueError: If the provided `uid` is already used or not valid
            DataVizException: if the visualization is locked
        :return: `True` if the visualisation was successfully stored.
        :rtype: bool
        """
        # Check UID pattern
        if not re.match(UID_PATTERN, uid):
            error = 'uid not valid. '
            error += "It can only contain alphanumeric characters, plus '-' and '_'"

            raise ValueError(error)

        if not (uid and title and dash_app):
            raise ValueError('Missing parameter')

        is_new = True

        # Here we search only by uid and not also by user,
        # since we want to make sure there aren't other viz stored
        # with the same uid
        record = self._collection.find_one({'uid': uid})

        if record:
            # Just check if the user is the one who created the viz
            if record['user'] and self.user != record['user']:
                raise ValueError(f"Viz '{uid}' already exists!")

            # Check if the viz it's locked
            if record['locked']:
                raise DataVizException('This viz is locked!')

            is_new = False

        # Store
        doc = {
            'uid': uid,
            'title': title,
            'user': self.user,
            'dashapp': dashapp_serializer(dash_app),
            #'app_prev': ,
            #'createdAt': ,
            #'updatedAt': ,
            'locked': locked,
            'tags': tags
        }

        if is_new:
            doc['dashapp_prev'] = None

            now = datetime.utcnow()
            doc['createdAt'] = now
            doc['updatedAt'] = now

        else:
            doc['dashapp_prev'] = record['dashapp']
            doc['updatedAt'] = datetime.utcnow()

        res = self._collection.update_one({'uid': uid, 'user': self.user}, {'$set': doc}, upsert=True)

        return bool(res)

    def load(self, uid: str) -> Optional[dict]:
        """Inverse process of storing: retrieve a visualisation from the database
        to display it on the web.

        :param name: visualisation's unique identifier
        :type name: str
        :return: All visualisation's information. `None` if no visualisation is found.
        :rtype: Optional[dict]
        """
        record = self._collection.find_one({'uid': uid, 'user': self.user})
        if not record:
            return None

        return self._clean_record(record)

    def restore(self, uid: str) -> bool:
        """Restore the visualization using the previous stored data.
        Works only once.

        :param uid: visualisation's unique identifier
        :type uid: str
        :return: `True` if the visualisation was successfull
        :rtype: bool
        """
        record = self._collection.find_one({'uid': uid, 'user': self.user})
        if (not record) or (not record['dashapp_prev']):
            return False

        doc = {
            'dashapp': record['dashapp_prev'],
            'dashapp_prev': None
        }
        res = self._collection.update_one({'uid': uid, 'user': self.user}, {'$set': doc}, upsert=False)

        return bool(res)

    def delete(self, uid: str, ask_confirm=True) -> bool:
        """Delete a visualization (only if not locked).

        :param uid: visualization unique identifier
        :type uid: str
        :param ask_confirm: Ask a confirmation from the user, using the builtin `input` function.
            The only correct answer is 'yes', anything else will cancel the deletion.
            Defaults to `True`.
        :type ask_confirm: bool, optional
        :raises: DataVizException: if the visualization is locked
        :return: `True` if the operation was successful
        :rtype: bool
        """
        record = self._collection.find_one({'uid': uid, 'user': self.user})
        if not record:
            return False

        # Ask for a confirmation to prevent unwanted deletions
        if ask_confirm:
            answer = input(f"Are you sure to delete viz '{uid}' (yes/no)?")

            if answer != 'yes':
                return False

        # Check if the viz is locked
        if record['locked']:
            raise DataVizException('This viz is locked!')

        # Delete
        res = self._collection.delete_one({'uid': uid, 'user': self.user})

        return bool(res)

    def lock(self, uid: str) -> bool:
        """Lock a visualization.
        A locked visualization cannot be modifed or deleted. To unlock it, use the
        `DataViz.unlock` method.

        :param uid: visualization unique identifier
        :type uid: str
        :return: True` if the operation was successful
        :rtype: bool
        """
        record = self._collection.find_one({'uid': uid, 'user': self.user})

        if not record:
            logger.warning(f"'{uid}' not found")
            return False

        doc = {'locked': True}

        res = self._collection.update_one({'uid': uid, 'user': self.user}, {'$set': doc}, upsert=False)

        return bool(res)

    def unlock(self, uid: str) -> bool:
        """Unlock a visualization. The inverse process of `DataViz.unlock`.

        :param uid: visualization unique identifier
        :type uid: str
        :return: True` if the operation was successful
        :rtype: bool
        """
        record = self._collection.find_one({'uid': uid, 'user': self.user})

        if not record:
            logger.warning(f"'{uid}' not found")
            return False

        doc = {'locked': False}

        res = self._collection.update_one({'uid': uid, 'user': self.user}, {'$set': doc}, upsert=False)

        return bool(res)

    def check_uid_availability(self, uid: str) -> bool:
        """Check if there's already a visualization stored with this `uid`.

        :param uid: An identifier.
        :type uid: str
        :return: True if no visualisation has been found.
        :rtype: bool
        """
        record = self._collection.find_one({'uid': uid})

        return not bool(record)

    def is_db_connected(self) -> bool:
        """Returns `True` if the database is connected.
        Note: the connection is established asynchronously so if the function is called
        right after the creation of the object it may return `False` while in fact the
        connection is in its way.

        :return: True if the database is connected.
        :rtype: bool
        """
        try:
            self._client.admin.command('ismaster')
            return True

        except ConnectionFailure:
            return False

    def get_my_visualisations(self) -> List[dict]:
        """Get the visualizations created by this user.

        :return: List of visualizations made by the current user.
        :rtype: list of dict
        """
        results = self._collection.find({'user': self.user})

        if not results:
            return []

        return [self._clean_record(record) for record in results]

    def _clean_record(self, record: dict) -> dict:
        if not record:
            return record

        cleaned = record.copy()

        # Remove internal Mongo ID and user info
        cleaned.pop('_id')
        cleaned.pop('user')

        # Remove dashapp_prev too, it's for internal use
        cleaned.pop('dashapp_prev')

        # Deserialize app
        cleaned['dashapp'] = dashapp_deserializer(record['dashapp'])

        return cleaned

    def __repr__(self):
        return 'DataViz(user="{}", db_name="{}", col_name="{}")'.format(self.user, self._db_name, self._collection_name)

    def __str__(self):
        return 'DataViz(user={}, db_name={}, col_name={})'.format(self.user, self._db_name, self._collection_name)
