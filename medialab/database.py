# Generic
import os
import logging
import pickle
from typing import Optional, Any
from datetime import datetime

# Connection with Mongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
import bson

# Plotly's Dash
import dash
dash_component_type = dash.development.base_component.ComponentMeta

from .utils import generate_uid

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(os.getenv('LOG_LEVEL', 'WARNING').upper())


class DatabaseError(Exception):
    """Base class for database exceptions"""

class UIDAlreadyExists(DatabaseError):
    """Raised when the UID already exists on the database."""


class Database:
    """Allows to store and retrieve a visualisation on a Mongo database. """

    __DB_NAME = 'notebook'
    __COLLECTION_NAME = 'apps'
    __RAW_LAYOUT_FIELD = 'raw'
    __RAW_LAYOUT_SIZE_WARNING = 40   # kilobytes

    def __init__(self, uri: Optional[str] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self.db = self.client[self.__DB_NAME]

    def store_visualisation(self, uid: str, title: str, description: str, author: str,
        layout: dash_component_type, active: bool = True) -> bool:
        """Stores a visualisation onto the database in order to be retrieved later on the web.

        :param uid: visualisation's unique identifier
        :type uid: str
        :param title: visualisation's title
        :type title: str
        :param description: brief description
        :type description: str
        :param author: author of the visualisation
        :type author: str
        :param layout: Dash's layout containing the visualisation
        :type layout: dash_component_type
        :param active: set this to `False` will cause the visualisation to be purged
            from the database after 24h
        :type active: bool

        :raises UIDAlreadyExists: UID is already registered from another author

        :return: True if the visualisation was stored successfully.
        :rtype: bool
        """
        collection = self.db[self.__COLLECTION_NAME]

        # Prevent one author to override another author's visualisation
        record = collection.find_one({'uid': uid})
        if record and (author != record['author']):
            raise UIDAlreadyExists(f'UID <{uid}> is already registered from another author!')

        # Display warning message for large layouts
        raw_layout = self._serialise(layout)
        if len(raw_layout) // 1024 >= self.__RAW_LAYOUT_SIZE_WARNING:
            msg = f'Warning: serialised layout is larger than {self.__RAW_LAYOUT_SIZE_WARNING} KB. '
            msg += 'Large layouts will incrase the loading time of the final webpage.'
            logger.warning(msg)

        doc = {
            'uid': uid,
            'title': title,
            'description': description,
            'author': author,
            'raw': bson.Binary(raw_layout),
            'createdAt': datetime.utcnow(),
            'active': active
        }

        res = collection.update_one({'uid': uid}, {'$set': doc}, upsert=True)

        return bool(res)

    def load_visualisation(self, uid: str) -> Optional[dict]:
        """Inverse process of storing: retrieve a visualisation from the database
        to display it on the web.

        :param name: visualisation's unique identifier returned from `store_visualisation()`
        :type name: str
        :return: All visualisation's information: name, title, description, author and layout.
            None if no visualisation is found.
        :rtype: Optional[dict]
        """
        collection = self.db[self.__COLLECTION_NAME]

        if not collection:
            return None

        record = collection.find_one({'uid': uid})
        if not record:
            return None

        record['layout'] = pickle.loads(record[self.__RAW_LAYOUT_FIELD])

        # remove unwanted fields
        for key in ['_id', self.__RAW_LAYOUT_FIELD]:
            if key in record:
                record.pop(key)

        return record

    def is_connected(self) -> bool:
        """Check the connection with the database.
        Note: the connection is established asynchronously so if the function is called
        right after the creation of the object it may return `False` while in fact the
        connection is in its way.

        :return: True if the database is connected.
        :rtype: bool
        """
        try:
            self.client.admin.command('ismaster')
            return True

        except ConnectionFailure:
            return False

    @classmethod
    def _serialise(cls, data: Any) -> bytes:
        return pickle.dumps(data)

    @classmethod
    def _deserialise(cls, raw_data: bytes) -> Any:
        return pickle.loads(raw_data)

    def __repr__(self):
        return "Database(host='%s:%s')" % (self.client.HOST, self.client.PORT)
