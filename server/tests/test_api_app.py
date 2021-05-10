import json
import pytest

from dataviz_server.api_app import create_app, VISUALISATIONS_ROUTE
from dataviz_server.api_app import pymongo

BAD_TAGS_PARAM = '?tags=bad1'

@pytest.fixture
def app(mocker):
    mock_collection = mocker.patch.object(pymongo.collection, 'Collection')
    app = create_app(mock_collection)
    app.debug = True

    return app.test_client()

def test_visualisations_endpoint_returns_json(app):
    res = app.get(VISUALISATIONS_ROUTE)

    assert res.mimetype == 'application/json'

def test_visualisations_endpoint_sanitisation(app):
    res = app.get(VISUALISATIONS_ROUTE + BAD_TAGS_PARAM)

    assert res.get_json() == []
