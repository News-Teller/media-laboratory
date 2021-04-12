import pytest
import plotly
import json

from dataviz.serializer import dashapp_serializer, dashapp_deserializer
from tests.assets.simple_app import app

def test_serializer():
    serialized = dashapp_serializer(app)
    new_app = dashapp_deserializer(serialized)

    # see if attributes were restored
    for attr in app.config.keys():
        assert app.config.get(attr) == new_app.config.get(attr)

    # check json-serialized layout
    layout = json.dumps(app.layout, cls=plotly.utils.PlotlyJSONEncoder)
    new_layout = json.dumps(app.layout, cls=plotly.utils.PlotlyJSONEncoder)
    assert layout == new_layout

    # assert index page
    assert app.index_string == new_app.index_string
