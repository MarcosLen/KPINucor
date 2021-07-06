import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output
from callbacks import title_labels
from datetime import date
from controls import recipes_options, pool_dict

app.config.suppress_callback_exceptions = True

label_style = {'text-align': 'center', 'text-decoration': 'bold', 'font-size': '4.5rem'}
div_style = {'width': '31%', 'margin': '0.5%', 'backgroundColor': 'white', 'padding': '1%'}
pool_div_style = {'margin': '0.5%', 'backgroundColor': 'white', 'width': '23%'}

body = html.Div([
    html.Div([], className='col-1'),
    html.Div([
        dbc.Tabs(id='tab_selector', active_tab='tab1', children=[
            dbc.Tab(label='General information', tab_id='tab1'),
            dbc.Tab(label='Pools', tab_id='tab2'),
            dbc.Tab(label='Bundles', tab_id='tab3'),
            dbc.Tab(label='Trolleys', tab_id='tab4'),
        ], className='nav nav-tabs', style={'font-size': 18}),

        html.Div([  # first row
            html.Div([
                html.H3(id='title_label_1', style={'margin-left': 7, 'margin-top': '0.5%'}),
                html.H1(id="value_label_1", style=label_style)
            ], className="col-3", style=div_style),
            html.Div([
                html.H3(id='title_label_2', style={'margin-left': 7, 'margin-top': '0.5%'}),
                html.H1(id="value_label_2", style=label_style)
            ], className="col-3", style=div_style),
            html.Div([
                html.H3(id='title_label_3', style={'margin-left': 7, 'margin-top': '0.5%'}),
                html.H1(id="value_label_3", style=label_style)
            ], style=div_style),
        ], className='row bs-component', style={'margin-top': '0.5%', 'margin-bottom': '0%'}),

        html.Div([  # second row
            html.Div([
                html.H2('Filtering', style={'margin-top': '0.5%'}),
                html.H3('Date range: ', style={'margin-left': 15, 'margin-top': 5, 'text-decoration': 'bold'}),
                dcc.DatePickerRange(
                    id='date_picker',
                    min_date_allowed=date(2021, 1, 1),
                    max_date_allowed=date(2021, 12, 31),
                    initial_visible_month=date(2021, 5, 1),
                    start_date=date(2021, 5, 1),
                    end_date=date(2021, 5, 31),
                    className='dash-bootstrap',
                    style={'margin-left': 15}
                ),
                html.H3('Shift: ', style={'margin-left': 15, 'margin-top': 15, 'text-decoration': 'bold'}),
                dbc.Checklist(id='filter-checklist', options=[
                    {'label': '      Morning', 'value': 'MS'},
                    {'label': '      Afternoon', 'value': 'AS'},
                    {'label': '      Night', 'value': 'NS'},
                ], value=['MS', 'AS', 'NS'], style={'margin-left': 15}),  # , className='form-check', inputClassName='form-check-input', labelClassName='form-check-label'),
                html.Div([
                    html.H3('Recipe: ', style={'margin-left': 15, 'margin-top': 15, 'text-decoration': 'bold'}),
                    dbc.Select(id='filter_dropdown', options=recipes_options, value='All', style={'margin-left': 15}),
                ]),
                html.Div([
                    html.H3(id='extra_filter_p', style={'margin-left': 15, 'margin-top': 15, 'text-decoration': 'bold'}),
                    dbc.Select(id='extra_filter_dropdown', value='All', style={'margin-left': 15}),
                ], id='extra_filter', hidden=False)

            ], style=div_style),


            html.Div([
                dcc.Graph(id='main_graph', style={'height': 365, 'display': 'inline-block', 'width': '100%'},
                          config={'displayModeBar': False, 'showTips': False})
            ], style={'margin': '0.5%', 'margin-left': '0%', 'width': '64.5%'}),
        ], className='row'),

        html.Div([  # third row
            html.Div([  # 3rd row for trolley tab
                html.Div([
                    dcc.Graph(id='small_graph_1', style={'height': 300, 'width': '100%'},
                              config={'displayModeBar': False, 'showTips': False})
                ], style={'width': '31.5%', 'margin': '0.5%', 'margin-right': '1%', 'backgroundColor': 'white'}),
                html.Div([
                    dcc.Graph(id='small_graph_2', style={'height': 300, 'width': '100%'},
                              config={'displayModeBar': False, 'showTips': False})
                ], style={'width': '31%', 'margin': '0.5%', 'backgroundColor': 'white'}),
                html.Div([
                    dcc.Graph(id='small_graph_3', style={'height': 300, 'width': '100%'},
                              config={'displayModeBar': False, 'showTips': False})
                ], style=div_style),
                ], id='div3_trolley', hidden=True, className='row col-12'),

            html.Div([  # 3rd row for pool tab --> all 16 pool in 2 for loops
                html.Div([
                    html.Div([
                        html.H3('{}'.format(pool_dict[4*i+j+1]['label']),
                                style={'margin-bottom': '1%', 'margin-top': '1%',
                                       'text-align': 'center', 'text-decoration': 'underline'}),
                        dcc.Graph(id='pool_graph{}'.format(4*i+j+1), style={'height': 130, 'width': '100%'},
                                  config={'displayModeBar': False, 'showTips': False}),
                        html.H4('Processed bundles: ', style={'display': 'inline-block'}),
                        html.H4(id='label1_pool{}'.format(4*i+j+1), style={'text-decorator': 'bold'}),
                        html.H4('Processed surface: ', id='label2_pool{}'.format(4*i+j+1)),
                        html.H4('Processed weight: ', id='label3_pool{}'.format(4*i+j+1))
                    ], style=pool_div_style)
                for j in range(4)], className='row col-12')
            for i in range(4)], id='div3_pool', hidden=False)

        ], className='row')  # , style={'margin-top': '1%', 'margin-bottom': '1%'})
    ], className='col-10 bs-component', style={}),

    # html.Div([], className='col-1')  # column for right margin

], className='row', style={'margin-top': '1%', 'margin-bottom': '1%'})

header = html.Div([
    html.Div([
        html.Img(
                src='/assets/images/logo-nucor.jpg',
                height='53 px',
                width='auto')
        ], className='col-2', style={'textAlign': 'center',
                                     'padding-top': '0.45%',
                                     'height': 'auto'}),
    html.Div([
        html.H1(
            children='Performance Dashboard',
            style={'textAlign': 'center', 'margin-top': 20, 'font-size': 35}
        )
    ], className='col-8'),
    html.Div([
        html.Img(
                src='/assets/images/kupner-logo.jpeg',
                height='53 px',
                width='auto')
        ], className='col-2', style={'align-items': 'center',
                                     'padding-top': '0.45%',
                                     'height': 'auto'})
    ],
    className='row',
    style={'height': '1%'}
)
