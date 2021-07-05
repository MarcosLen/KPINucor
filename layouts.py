import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output
from callbacks import title_labels
from datetime import date
from controls import recipes_options, pool_dict

app.config.suppress_callback_exceptions = True

label_style = {'text-align': 'center', 'text-decoration': 'bold', 'font-size': '2.5rem'}

body = html.Div([
    html.Div([], className='col-1'),
    html.Div([
        dbc.Tabs(id='tab_selector', active_tab='tab1', children=[
            dbc.Tab(label='General information', tab_id='tab1', active_tab_style={'backgroundColor': '#F9F9F9'}),
            dbc.Tab(label='Pools', tab_id='tab2'),
            dbc.Tab(label='Bundles', tab_id='tab3'),
            dbc.Tab(label='Trolleys', tab_id='tab4'),
        ], className='nav nav-tabs', style={'font-size': 25, 'justify-content': 'center'}),

        html.Div([  # first row
            html.Div([
                html.H4(id='title_label_1', style={'margin-left': 7}),
                html.H1(id="value_label_1", style=label_style)
            ], className="pretty_container bs-component", style={'width': '31%'}),
            html.Div([
                html.H4(id='title_label_2', style={'margin-left': 7}),
                html.H1(id="value_label_2", style=label_style)
            ], className="pretty_container bs-component", style={'width': '31%'}),
            html.Div([
                html.H4(id='title_label_3', style={'margin-left': 7}),
                html.H1(id="value_label_3", style=label_style)
            ], className="pretty_container", style={'width': '31%'}),
        ], className='row bs-component', style={'margin-top': '0.5%', 'margin-bottom': '1%'}),

        html.Div([  # second row
            html.Div([
                html.H2('Filtering:', style={'text-align': 'center'}),
                html.H4('Date range: ', style={'margin-left': 15, 'margin-top': 5, 'text-decoration': 'bold'}),
                dcc.DatePickerRange(
                    id='date_picker',
                    min_date_allowed=date(2021, 1, 1),
                    max_date_allowed=date(2021, 12, 31),
                    initial_visible_month=date(2021, 5, 1),
                    start_date=date(2021, 5, 1),
                    end_date=date(2021, 5, 31),
                    className='dash-bootstrap'
                ),
                html.H4('Shift: ', style={'margin-left': 15, 'margin-top': 10, 'text-decoration': 'bold'}),
                dbc.Checklist(id='filter-checklist', options=[
                    {'label': '      Morning', 'value': 'MS'},
                    {'label': '      Afternoon', 'value': 'AS'},
                    {'label': '      Night', 'value': 'NS'},
                ], value=['MS', 'AS', 'NS']),  # , className='form-check', inputClassName='form-check-input', labelClassName='form-check-label'),
                html.Div([
                    html.H4('Recipe: ', style={'margin-left': 15, 'margin-top': 10, 'text-decoration': 'bold'}),
                    dbc.Select(id='filter_dropdown', options=recipes_options, value='All'),
                    # dcc.Dropdown(
                    #     id='filter_dropdown',
                    #     options=recipes_options,
                    #     multi=False,
                    #     value='All',
                    #     className="dcc_control"
                    # )
                ]),
                html.Div([
                    html.H4(id='extra_filter_p', style={'margin-left': 15, 'margin-top': 10, 'text-decoration': 'bold'}),
                    dbc.Select(id='extra_filter_dropdown', value='All'),
                    # dcc.Dropdown(
                    #      id='extra_filter_dropdown',
                    #      multi=False,
                    #      value='All',
                    #      className="dcc_control"
                    #      )
                ], id='extra_filter', hidden=False)

            ], className='pretty_container', style={'width': '31%'}),


            html.Div([
                dcc.Graph(id='main_graph', style={'height': 360, 'display': 'inline-block', 'width': '100%'},
                          # figure={'layout': {'paper_bgcolor': '#F9F9F9', 'plot_bgcolor': '#F9F9F9'}},
                          config={'displayModeBar': False, 'showTips': False})
            ], style={'margin-left': '1%', 'margin-right': '1%', 'width': '63%'}),
        ], className='row'),

        html.Div([  # third row
            html.Div([  # 3rd row for trolley tab
                html.Div([
                    dcc.Graph(id='small_graph_1', style={'height': 300, 'width': '100%'},
                              config={'displayModeBar': False, 'showTips': False})
                ], className='col-4'),
                html.Div([
                    dcc.Graph(id='small_graph_2', style={'height': 300, 'width': '100%'},
                              config={'displayModeBar': False, 'showTips': False})
                ], className='col-4'),
                html.Div([
                    dcc.Graph(id='small_graph_3', style={'height': 300, 'width': '100%'},
                              config={'displayModeBar': False, 'showTips': False})
                ], className='col-4'),
                ], id='div3_trolley', hidden=True, className='row col-12'),

            html.Div([  # 3rd row for pool tab --> all 16 pool in 2 for loops
                html.Div([
                    html.Div([
                        html.H3('{}'.format(pool_dict[4*i+j+1]['label']),
                                style={'margin-bottom': '1%', 'margin-top': '10%',
                                       'text-align': 'center', 'text-decoration': 'underline'}),
                        # html.H5('Temperature: '),
                        dcc.Graph(id='pool_graph{}'.format(4*i+j+1), style={'height': 150, 'width': '100%'},
                                  config={'displayModeBar': False, 'showTips': False}),
                        html.H4('Processed bundles: ', id='label1_pool{}'.format(4*i+j+1)),
                        html.H5('Processed surface: ', id='label2_pool{}'.format(4*i+j+1)),
                        html.H5('Processed weight: ', id='label3_pool{}'.format(4*i+j+1))
                    ], className='col-3')
                for j in range(4)], className='row col-12')
            for i in range(4)], id='div3_pool', hidden=False, className='row col-12')

        ], className='row', style={'margin-top': '1%', 'margin-bottom': '1%'})
    ], className='pretty_container col-10 bs-component', style={}),

    html.Div([], className='col-1')  # column for right margin

], className='row', style={'margin-top': '1%', 'margin-bottom': '1%'})

header = html.Div([
    html.Div([
        html.Img(
                src='/assets/images/logo-nucor.jpg',
                height='43 px',
                width='auto')
        ], className='col-2', style={'textAlign': 'center',
                                     'padding-top': '0.45%',
                                     'height': 'auto'}),
    html.Div([
        html.H1(
            children='Performance Dashboard',
            style={'textAlign': 'center', 'margin-top': 20}
        )
    ], className='col-8'),
    html.Div([
        html.Img(
                src='/assets/images/kupner-logo.jpeg',
                height='43 px',
                width='auto')
        ], className='col-2', style={'align-items': 'center',
                                     'padding-top': '0.45%',
                                     'height': 'auto'})
    ],
    className='row',
    style={'height': '1%'}
)
