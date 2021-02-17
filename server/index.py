# Generic
import os
import logging

# Plotly's Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import redirect

# our module
from app import app, server
from database import Database, DatabaseError

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO').upper())

# Create the database
db = Database()

# Webpage main layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# On the index page just show a working message
index_layout = html.Div('It works!')

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return index_layout

    # url example: 'http://example.com/:uid'
    visualisation_uid = pathname[1:]

    try:
        record = db.load_visualisation(visualisation_uid)
        if record:
            app.title = record['title']
            app.description = record['description']

            return record['layout']

        else:
            return '404'

    except DatabaseError as err:
        logger.warning(err)
        return '404'

# Run this on developing/test
if __name__ == '__main__':
    app.run_server()
