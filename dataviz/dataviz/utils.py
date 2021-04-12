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
