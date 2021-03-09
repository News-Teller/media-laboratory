# Generic
import os

# Plotly's Dash
from dash import Dash
import dash_bootstrap_components as dbc

# Cache
from flask_caching import Cache

class CustomDash(Dash):
    """Custom Dash app which overrides the default HTML index template. """

    def interpolate_index(self, **kwargs):
        return '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>{title}</title>
                {metas}
                <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg" />
                <link rel="alternate icon" href="/assets/favicon.ico" />
                {css}
            </head>
            <body>
                {app_entry}
                {config}
                {scripts}
                {renderer}
            </body>
        </html>
        '''.format(**kwargs)


title = 'Media-Laboratory'
description = '''
Data visualisation tool to share your visual analysis on the Web, allowing a smooth transition from experiments to production.
'''
meta_tags = [
    {'name': 'description', 'content': description},
    {'name': 'viewport', 'content':'width=device-width, initial-scale=1.0'},
    {'property': 'og:title', 'content': title},
    {'property': 'og:description', 'content': description},
    {'property': 'og:type', 'content': 'website'},
    {'name': 'robots', 'content': 'noindex, follow'}
]
app = CustomDash(
    __name__,
    title=title,
    meta_tags=meta_tags,
    update_title='Loading...',
    serve_locally=False,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
server = app.server

# Use Flask-Caching library to save callback results in a shared memory
TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 60 * 2))   # in seconds
cache = Cache(app.server, config={
    'DEBUG': True if os.getenv('DEBUG') == 'True' else False,
    'CACHE_TYPE': 'filesystem',
    'CACHE_DEFAULT_TIMEOUT': TIMEOUT,
    'CACHE_DIR': '.cache'
})

# Alias cache decorator here for clarity
mycache = cache.memoize(timeout=TIMEOUT)
