import os
from typing import Optional

# Flask app configs
class Config:
    ENV = 'production'
    TESTING = False
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DEBUG = False
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

class LocalConfig(Config):
    ENV = 'development'
    DEBUG = True
    CACHE_TYPE = 'NullCache'

class TestConfig(Config):
    ENV = 'development'
    TESTING = True
    MONGODB_URI = 'mongodb://localhost:27017/'
    CACHE_TYPE = 'NullCache'


# dash-app server-side config to work with the dispatcher
def build_dashapp_server_configs(app_name: str) -> dict:
    config = {
        'name': app_name,
        #'assets_folder':,
        'serve_locally': False,
        'requests_pathname_prefix': f'/{app_name}/'
    }

    # override root asset folder, from local dev (client) to prod (server) location
    # MAP_ASSETS_FOLDER=<current>:<to-change>
    if os.getenv('MAP_ASSETS_FOLDER'):
        old, new = os.getenv('MAP_ASSETS_FOLDER').split(':')
        if old and new:
            config['assets_folder'] = lambda assets_folder: assets_folder.replace(old, new)

    if os.getenv('DASH_ASSETS_EXTERNAL_PATH'):
        config['assets_external_path'] = os.getenv('DASH_ASSETS_EXTERNAL_PATH')

    return config
