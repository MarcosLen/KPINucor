import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

from app import app
import layouts

app.config.suppress_callback_exceptions = True

index_page = html.Div([
    dcc.Location(id='url', pathname='/kpi', refresh=True),
    layouts.header,
    html.Hr(),
    layouts.body,
    html.Div([

    ], style={})
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/kpi':
        return index_page
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)
