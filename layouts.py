import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output
from callbacks import title_labels
from datetime import date
from controls import recipes_options, pool_dict

app.config.suppress_callback_exceptions = True

# label_style = {'text-align': 'center', 'text-decoration': 'bold', 'font-size': '4.5rem'}
# div_style = {'width': '31%', 'margin': '0.5%', 'backgroundColor': 'white', 'padding': '1%'}
# pool_div_style = {'margin': '0.5%', 'backgroundColor': 'white', 'width': '23%'}
head_div_style = {'padding': '0.25%', 'text-align': 'center'}
div_style = {'padding': '0.25%', 'background-color': '#fff'}
big_div_style = {'padding': '0.25%', 'padding-top': '0.5%', 'padding-bottom': '0.5%'}


def pool_div(i):
    return html.Div([
        html.H4('{}'.format(pool_dict[i]['label']),
                style={'text-decoration': 'underline', 'margin-left': '1%'}),
        dcc.Graph(id='pool_graph{}'.format(i), style={'height': 120},
                  config={'displayModeBar': False, 'showTips': False}),
        html.Div([
            html.H6('Processed bundles: ', className='col-auto', style={'margin-left': '2%'}),
            html.H6(id='label1_pool{}'.format(i), className='col-auto', style={'font-weight': 'bolder'}),
        ], className='row align-items-start'),
        html.Div([
            html.H6('Processed surface: ', className='col-auto', style={'margin-left': '2%'}),
            html.H6(id='label2_pool{}'.format(i), className='col-auto', style={'font-weight': 'bolder'}),
        ], className='row align-items-start'),
        html.Div([
            html.H6('Processed weight: ', className='col-auto', style={'margin-left': '2%'}),
            html.H6(id='label3_pool{}'.format(i), className='col-auto', style={'font-weight': 'bolder'}),
        ], className='row align-items-start'),
    ], style=div_style)


index_page = html.Div([
    html.Div([
        dcc.Location(id='url', pathname='/kpi', refresh=True),
        html.Div([
            html.Img(src='/assets/images/logo-nucor.jpg', height='58 px', width='auto')
        ], className='col-2', style=head_div_style),
        html.Div([
            html.H1('Performance Dashboard')
        ], className='col-8'),
        html.Div([
            html.Img(src='/assets/images/kupner-logo.jpeg', height='53 px', width='auto')
        ], className='col-2', style=head_div_style)
    ], className='row align-items-center', style=head_div_style),  # header
    html.Hr(),

    html.Div([
        dbc.Tabs(id='tab_selector', active_tab='tab1', children=[
            dbc.Tab(label='General information', tab_id='tab1'),
            dbc.Tab(label='Pools', tab_id='tab2'),
            dbc.Tab(label='Bundles', tab_id='tab3'),
            dbc.Tab(label='Trolleys', tab_id='tab4'),
        ], className='nav nav-tabs'),

        html.Div([  # first row
            html.Div([
                html.Div([html.Div([
                    html.H3(id='title_label_1', style={'margin-left': '2%'}),
                    html.H1(id="value_label_1", style={'text-align': 'center'})
                    ], style=div_style)], className='col-4 pr-0'),
                html.Div([html.Div([
                    html.H3(id='title_label_2', style={'margin-left': '2%'}),
                    html.H1(id="value_label_2", style={'text-align': 'center'})
                ], style=div_style)], className='col-4 px-0'),
                html.Div([html.Div([
                    html.H3(id='title_label_3', style={'margin-left': '2%'}),
                    html.H1(id="value_label_3", style={'text-align': 'center'})
                ], style=div_style)], className='col-4 pl-0'),
            ], className='row'),
        ], style=big_div_style),  # first row

        html.Div([  # second row
            html.Div([
                html.Div([  # filter div
                    html.Div([
                        html.H4('Filtering', style={'margin-left': '2%'}),
                        html.Div([
                            html.H5('Date range: ', style={'margin-left': 15, 'margin-top': 5, 'text-decoration': 'bold'}),
                            dcc.DatePickerRange(
                                id='date_picker',
                                min_date_allowed=date(2021, 1, 1),
                                max_date_allowed=date(2021, 12, 31),
                                initial_visible_month=date(2021, 5, 1),
                                start_date=date(2021, 5, 1),
                                end_date=date(2021, 5, 31),
                                className='dash-bootstrap',
                                style={'margin-left': '5%'}
                                ),
                            html.H5('Shift: '),
                            dbc.Checklist(id='filter-checklist', options=[
                                {'label': '      Morning', 'value': 'MS'},
                                {'label': '      Afternoon', 'value': 'AS'},
                                {'label': '      Night', 'value': 'NS'},
                            ], value=['MS', 'AS', 'NS'], style={'margin-left': '5%'}),
                            html.Div([
                                html.H5('Recipe: '),
                                dbc.Select(id='filter_dropdown', options=recipes_options, value='All',
                                           style={'margin-left': '5%'}),
                            ]),
                            html.Div([
                                html.H5(id='extra_filter_p'),
                                dbc.Select(id='extra_filter_dropdown', value='All', style={'margin-left': '5%'}),
                            ], id='extra_filter', hidden=False)
                        ], style={'margin-left': '5%'}),
                    ], className='h-100', style=div_style)
                ], className='col-4'),  # filter div

                html.Div([  # main graph div
                    html.Div([
                        dcc.Graph(id='main_graph', style={'height': 365},
                                  config={'displayModeBar': False, 'showTips': False})
                        ], className='h-100', style={'padding-left': 0}),
                ], className='col-8', style={'padding-left': 0}),
            ], className='row'),  # main graph div
        ], style=big_div_style),  # second row

        html.Div([  # third row for trolley tab
            html.Div([
                html.Div([html.Div([
                    dcc.Graph(id='small_graph_1', style={'height': 300},
                              config={'displayModeBar': False, 'showTips': False})
                ], style=div_style)], className='col-4 pr-0'),
                html.Div([html.Div([
                    dcc.Graph(id='small_graph_2', style={'height': 300},
                              config={'displayModeBar': False, 'showTips': False})
                ], style=div_style)], className='col-4 px-0'),
                html.Div([html.Div([
                    dcc.Graph(id='small_graph_3', style={'height': 300},
                              config={'displayModeBar': False, 'showTips': False})
                ], style=div_style)], className='col-4 pl-0'),
            ], className='row'),
        ], id='div3_trolley', hidden=True, style=big_div_style),  # third row for trolley tab

        html.Div([  # pool row
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([pool_div(1)], className='col-3 px-1'),
                        html.Div([pool_div(2)], className='col-3 px-1'),
                        html.Div([pool_div(3)], className='col-3 px-1'),
                        html.Div([pool_div(4)], className='col-3 px-1'),
                    ], className='row p-1 px-2'),
                    html.Div([
                        html.Div([pool_div(5)], className='col-3 px-1'),
                        html.Div([pool_div(6)], className='col-3 px-1'),
                        html.Div([pool_div(7)], className='col-3 px-1'),
                        html.Div([pool_div(8)], className='col-3 px-1'),
                    ], className='row p-1 px-2'),
                    html.Div([
                        html.Div([pool_div(9)], className='col-3 px-1'),
                        html.Div([pool_div(10)], className='col-3 px-1'),
                        html.Div([pool_div(11)], className='col-3 px-1'),
                        html.Div([pool_div(12)], className='col-3 px-1'),
                    ], className='row p-1 px-2'),
                    html.Div([
                        html.Div([pool_div(13)], className='col-3 px-1'),
                        html.Div([pool_div(14)], className='col-3 px-1'),
                        html.Div([pool_div(15)], className='col-3 px-1'),
                        html.Div([pool_div(16)], className='col-3 px-1'),
                    ], className='row p-1 px-2'),
                ])
            ], className='row')
        ], id='div3_pool', style=big_div_style, hidden=False)  # pools hardcoded

    ], className='row align-items-center', style=big_div_style),
], className='container')
