# Generic
import os

# Plotly's Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import redirect

# our module
from app import app, server
from database import Database


# Create database
db = Database()

# Webpage main layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Layout for the index page, just displays a working message
index_layout = html.Div([
    html.H3('It works!'),
])

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return index_layout

    # url example: 'http://example.com/:uid'
    visualisation_uid = pathname[1:]

    record = db.load_visualisation(visualisation_uid)
    if record:
        app.title = record['title']
        app.description = record['description']

        return record['layout']

    else:
        return '404'

# Run this on developing/test
if __name__ == '__main__':
    debug = True if os.getenv('DASH_DEBUG_MODE') == 'True' else False

    app.run_server(
        host=os.getenv('DASH_HOST'),
        debug=debug
    )
