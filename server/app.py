# Generic
import os

# Plotly's Dash
from dash import Dash

# Cache
from flask_caching import Cache

class CustomDash(Dash):
    """Custom Dash app which overrides the default HTML content. """

    def __init__(self, *args, description=None, **kwargs):
        self.description = description

        super().__init__(
            *args,
            external_stylesheets=['style.css'],
            update_title='Loading...',
            **kwargs)

    def interpolate_index(self, **kwargs):
        kwargs['description'] = self.description

        return '''
        <!DOCTYPE html>
        <html>
            <head>
                {metas}
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <meta name="description" content="{description}">
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

app = CustomDash(__name__, suppress_callback_exceptions=True)
app.title = 'Media-Laboratory'
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
