# Generic
import os
import logging
import pymongo
from werkzeug.serving import run_simple

# Dash-related packages
# Note: syntax needs to match the one use on app-creation (notebook) side
import dash
import jupyter_dash
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies
import dash_bootstrap_components as dbc
import dash_simple_map
import dash_table

from dataviz_server import Dispatcher

# Create the database
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
mongo = pymongo.MongoClient(mongodb_uri, serverSelectionTimeoutMS=2000)
db = mongo[os.getenv('MONGODB_DB_NAME', 'medialab')]
collection = db[os.getenv('MONGODB_COL_NAME', 'viz')]

# Dispatcher / main application
application = Dispatcher(collection)

# Run this while developing locally
if __name__ == '__main__':
    run_simple('localhost', 5000, application)
