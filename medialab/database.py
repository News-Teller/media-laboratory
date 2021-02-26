# Generic
import os
import pickle
from uuid import uuid4
from typing import Optional, Any
from datetime import datetime

# Connection with Mongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
import bson

# Plotly's Dash
import dash
dash_component_type = dash.development.base_component.ComponentMeta


# Create an alias for exceptions
DatabaseError = PyMongoError

class Database:
    """Allows to store and retrieve a visualisation on a Mongo database. """

    __DB_NAME = 'notebook'
    __COLLECTION_NAME = 'apps'
    __RAW_LAYOUT_FIELD = 'raw'
    __RAW_LAYOUT_SIZE_WARNING = 40   # kilobytes

    def __init__(self, uri: Optional[str] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self.db = self.client[self.__DB_NAME]

    def store_visualisation(self, title: str, description: str, author: str, layout: dash_component_type,
        public: bool=True, uid: Optional[str] = None) -> Optional[str]:
        """Stores a visualisation onto the database in order to be retrieved later on the web.

        :param title: visualisation's title which will appear in the HTML title tag
        :type title: str
        :param description: brief description which will appear in the HTML description metatag
        :type description: str
        :param author: author of the visualisation
        :type author: str
        :param layout: actual visualisation, in the form of a Dash layout
        :type layout: dash_component_type
        :param public: if the visualisation can be accessible publicly on the web, defaults to True
        :type public: bool, optional
        :param name: visualisation's identifier, used to override an exisiting visualisation
        :type name: Optional[str]
        :return: the unique identifier for the visualisation if it was stored successfully, `None` otherwise
        :rtype: Optional[str]
        """
        collection = self.db[self.__COLLECTION_NAME]

        if not collection:
            return None

        # Display warning message for large layouts
        raw_layout = self._serialise(layout)
        if len(raw_layout) // 1024 >= self.__RAW_LAYOUT_SIZE_WARNING:
            msg = f'Warning: serialised layout is larger than {self.__RAW_LAYOUT_SIZE_WARNING} KB. '
            msg += 'Large layouts will incrase the loading time of the final webpage.'
            print(msg)

        # Generate application identifier
        if not uid:
            uid = self._generate_uid()

        doc = {
            'uid': uid,
            'title': title,
            'description': description,
            'author': author,
            'raw': bson.Binary(raw_layout),
            'public': public,
        }

        res = collection.update_one({'uid': uid}, {'$set': doc}, upsert=True)

        return uid if res else None

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
    def _generate_uid(cls):
        # Generate uuid of 8 chars
        # Note: from our tests, we experienced 0 collision in 1M draws of 12-char uuids
        uuid_str = str(uuid4())
        return uuid_str[:8] + uuid_str[9:13]

    @classmethod
    def _serialise(cls, data: Any) -> bytes:
        return pickle.dumps(data)

    @classmethod
    def _deserialise(cls, raw_data: bytes) -> Any:
        return pickle.loads(raw_data)

    def __repr__(self):
        return "Database(host='%s:%s')" % (self.client.HOST, self.client.PORT)
