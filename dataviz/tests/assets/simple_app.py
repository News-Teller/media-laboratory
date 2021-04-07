from jupyter_dash import JupyterDash
import dash_html_components as html


def create_app(config: dict = {}):
    app = JupyterDash(__name__, **config)

    app.layout = html.H1('test')

    return app
