# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # DataViz
# The `dataviz` package allows you to store your Dash apps and make them accessible from the webserver. To know more of this webserver, check the `server` folder of this repo [here](https://github.com/News-Teller/media-laboratory/server).

# Now, let's create a simple Dash app as an example.

# %%
import dataviz

import jupyter_dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


# %%
# the following example is taken from https://dash.plotly.com/layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = jupyter_dash.JupyterDash(
    __name__,
    title = 'Hello Dash',
    external_stylesheets=external_stylesheets
)

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# %% [markdown]
# Use the `DataViz` class to manage your visualizations and the `store` method to save them in the database.
# The `uid` is used to uniquely identifies them across all users. It can only be composed by alphanumeric characters, underscores and dashes (regex `^[a-zA-Z0-9_-]+$`).
# You can use one of your choise (use `check_uid_availability` from `datavis.utils` to see if your name is available)
# or use the `generate_uid` function inside `dataviz.utils` to generate a random one.
# The `title` provided here doens't need to match the one of the app and it's only used to better distinguish the app among the others.

# Once it's store the app will be accessible at `http(s)://<server-name:port>/<uid>`.

# %%
dz = dataviz.DataViz()
dz.store(
    uid='example',
    title='example viz',
    dash_app=app,
    tags=['example']
)
