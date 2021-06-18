import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, serve_locally=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server
server.config.update(SECRET_KEY="nnnnnn")

app.config.suppress_callback_exceptions = True
app.title = 'Nucor KPI by Kupner'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
