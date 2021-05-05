# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # DataViz
# The `dataviz` package allows you to interact with the backend infrastructure, by storing your Plotly Dash apps and serve them with the server.
# To know more of the backend, check the `server` folder of this repo [here](https://github.com/News-Teller/media-laboratory/server).
#
# Let's create a simple Dash app as an example.

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

app = jupyter_dash.JupyterDash(__name__, external_stylesheets=external_stylesheets)

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
# Use `DataViz` to store the app on backend. The `uid` uniquely identifies the application within the ecosystem and can only be composed by alphanumeric characters, underscores and dashes (regex `^[a-zA-Z0-9_-]+$`).
# You can use the `generate_uid` function inside `dataviz.utils` to generate a random one.
# The `title` provided here doens't need to match the one of the app and it's only used to better distinguish the app among the others.
#
# Once it's store the app will be accessible at `http(s)://<server-name>/<uid>`.

# %%
dz = dataviz.DataViz()
# dz.store(
#     uid='example',
#     title='example viz',
#     dash_app=app,
#     tags=['notebook', 'example']
# )

# %% [markdown]
# The `DataViz` object accepts two parameters: `uri` and `user`. Both can be set directly or via environment variables.
# If you are not running this locally, for example on a JupyterHub provided by an organization such as NewsTeller's Lab, you should let the organization's team set them using the latter option (like in the example above).
# %% [markdown]
# ### HTML export
# `dataviz` also include a shortcut to generate an HTML page from a Plotly.js figure. If your visualization consists only of a plot you an use this feature to improve the performances of the final visualization.
# As opposed to the previous call, the one below will also generate an HTML file `<uid>.html` in the current folder (which could be overriden using the `HTML_EXPORTS_FOLDER` environment variable).

# %%
dz.store(
    uid='example',
    title='example viz',
    dash_app=app,
    tags=['notebook', 'example', 'export'],
    export_as_html=True,
    figure=fig,
)

# %% [markdown]
#

