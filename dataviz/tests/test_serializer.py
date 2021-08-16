import pytest
import plotly
import json

from dataviz.serializer import (dashapp_serializer, dashapp_deserializer,
    get_attr_from_serialized_dashapp)
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

    # assert callback map was restored
    for k, v in app.callback_map.items():
        assert k in new_app.callback_map
        for ki, vi in v.items():
            assert ki in new_app.callback_map[k]

            if ki != 'callback':
                assert vi == new_app.callback_map[k][ki]
            else:
                assert vi.__name__ == new_app.callback_map[k][ki].__name__


@pytest.mark.parametrize(
    'attr, expected',
    [
        ('index_string', app.index_string),
        ('layout', app.layout),
        ('css', app.css),
        ('scripts', app.scripts),
    ]
)
def test_get_attr_from_serialized_dashapp(attr, expected):
    serialized = dashapp_serializer(app)

    # cannot test equality since `Scripts` and `CSS` objects don't implement it
    assert type(get_attr_from_serialized_dashapp(serialized, attr)) == type(expected)
