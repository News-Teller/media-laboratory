import os
import re
import logging
from typing import Optional
from flask import Flask, request, escape, jsonify
from flask_cors import CORS
from flask_caching import Cache
from werkzeug.exceptions import ServiceUnavailable
import pymongo
# from dataviz import DataViz

from .config import Config
from .utils import parse_tags, build_list_query, parse_viz_records


VISUALISATIONS_ROUTE = '/visualizations'
TAGS_PARAM_PATTERN = re.compile('^[a-zA-Z]+$')

def create_app(collection: pymongo.collection.Collection, config: Optional[Config] = None) -> Optional[Flask]:
    if not collection:
        return None

    app = Flask(__name__)

    # See http://flask.pocoo.org/docs/latest/config/
    app.config.from_object(config or {})

    # See https://flask-caching.readthedocs.io/en/latest/index.html
    cache = Cache(app)

    # Setup cors headers to allow all domains
    # https://flask-cors.readthedocs.io/en/latest/
    CORS(app)

    # Visualisation's database (mongodb) collection
    app.collection = collection

    @cache.cached()
    def listing():
        # Check connection with db
        with app.app_context():
            if not app.collection:
                return ServiceUnavailable()

        # Get query parameter
        param = request.args.get('tags', default='', type=str)
        tags = parse_tags(param, TAGS_PARAM_PATTERN)

        # Get vizs from db
        query = build_list_query(tags)
        results = app.collection.find(query)
        if not results:
            return jsonify([])

        data = parse_viz_records(results)
        return jsonify(data)

    app.add_url_rule(rule=VISUALISATIONS_ROUTE, endpoint='visualisations', view_func=listing, methods=['GET'])

    return app
