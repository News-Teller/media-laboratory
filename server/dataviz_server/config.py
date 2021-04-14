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
        'requests_pathname_prefix': f'/{app_name}/',
        'suppress_callback_exceptions': True
    }

    if os.getenv('ROOT_ASSETS_FOLDER'):
        config['assets_folder'] = os.path.join(os.getenv('ROOT_ASSETS_FOLDER'), app_name)

    if os.getenv('DASH_ASSETS_EXTERNAL_PATH'):
        config['assets_external_path'] = os.getenv('DASH_ASSETS_EXTERNAL_PATH')

    return config
