from jupyter_dash import JupyterDash
import dash_html_components as html

app = JupyterDash(__name__)
app.layout = html.H1('test')
