# Generic
import os
import logging

# Plotly's Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components
import dash_simple_map
import dash_table
import dash_cytoscape as cyto
from flask import redirect

# our module
from app import app, server, mycache
from database import Database, DatabaseError

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO').upper())

# Create the database
db = Database()

# Webpage main layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(id='title-placeholder', style={'display':'none'}, **{'data-value': None}),
    html.Div(id='desc-placeholder', style={'display':'none'}, **{'data-value': None}),
    html.Div(id='blank-output', style={'display':'none'})
])

# Set document title and description from the `data-value` attributes
# of the `title-placeholder` and `desc-placeholder` divs.
# See assets/dash_clientside.js for the javascript-side of the code
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='setMeta'
    ),
    Output('blank-output', 'children'),
    [Input('title-placeholder', 'data-value'), Input('desc-placeholder', 'data-value')]
)

@app.callback(
    [Output('page-content', 'children'),
    Output('title-placeholder', 'data-value'),
    Output('desc-placeholder', 'data-value')],
    Input('url', 'pathname')
)
@mycache
def display_page(pathname):
    if pathname == '/':
        # On the index page just show a working message
        index_layout = html.Div('It works!')

        return index_layout, None, None

    # url example: 'http://example.com/:uid'
    visualisation_uid = pathname[1:]

    try:
        record = db.load_visualisation(visualisation_uid)
        if record:
            return record['layout'], record['title'], record['description']

        else:
            return '404', None, None

    except DatabaseError as err:
        logger.warning(err)
        return '404', None, None

# Run this on developing/test
if __name__ == '__main__':
    debug = True if os.getenv('DEBUG') == 'True' else False

    app.run_server(debug=debug)
