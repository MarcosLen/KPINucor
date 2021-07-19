from dash.dependencies import Input, Output

from app import app
from layouts import index_page

app.config.suppress_callback_exceptions = True


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/kpi':
        return index_page
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)
