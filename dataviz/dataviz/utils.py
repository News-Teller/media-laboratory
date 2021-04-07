from uuid import uuid4
from threading import Timer
import dill
from dash import Dash
from jupyter_dash import JupyterDash


def generate_uid() -> str:
    """Generate a 12-char uuid (universally unique identifier).

    :return: uuid
    :rtype: str
    """
    # Note: from our tests, we experienced 0 collision in 1M draws of 12-char uuids
    uuid_str = str(uuid4())
    return uuid_str[:8] + uuid_str[9:13]

def app_factory_checker(func):
    """Check if `func` returns a Dash object (either `dash.Dash` or `jupyter_dash.JupyterDash`).
    For more information, check https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories.

    :param func:
    :type func: Callable
    :return: True if `func` returns a Dash object
    :rtype: bool
    """
    app = func()

    return isinstance(app, Dash) or isinstance(app, JupyterDash)
