# Plotly's Dash
from dash import Dash

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
server = app.server
