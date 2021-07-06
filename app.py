import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

app = dash.Dash(__name__, serve_locally=True, suppress_callback_exceptions=True,)
                # external_stylesheets=[dbc.themes.LUX])

load_figure_template("minty")
server = app.server
server.config.update(SECRET_KEY="nnnnnn")

app.config.suppress_callback_exceptions = True
app.title = 'Nucor KPI by Kupner'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
