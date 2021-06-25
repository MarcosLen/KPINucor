import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output
from callbacks import title_labels
from datetime import date
from controls import recipes_options, pool_dict

app.config.suppress_callback_exceptions = True

body = html.Div([
    html.Div([], className='col-1'),
    html.Div([
        dcc.Tabs(id='tab_selector', value='tab2', children=[
            dcc.Tab(label='General information', value='tab1',
                    style={'backgroundColor': '#E7E7E7'},
                    selected_style={'backgroundColor': '#F9F9F9'}),
            dcc.Tab(label='Pools', value='tab2',
                    style={'backgroundColor': '#E7E7E7'},
                    selected_style={'backgroundColor': '#F9F9F9'}),
            dcc.Tab(label='Bundles', value='tab3',
                    style={'backgroundColor': '#E7E7E7'},
                    selected_style={'backgroundColor': '#F9F9F9'},),
            dcc.Tab(label='Trolleys', value='tab4',
                    style={'backgroundColor': '#E7E7E7'},
                    selected_style={'backgroundColor': '#F9F9F9'},),
        ]),

        html.Div([  # first row
            html.Div([
                html.P(id='title_label_1'),
                html.H6(id="value_label_1",
                        style={'text-align': 'center', 'font-size': 30,
                               'text-decoration': 'bold', 'margin-right': '20%'})
            ], className="pretty_container", style={'width': '31%'}),
            html.Div([
                html.P(id='title_label_2'),
                html.H6(id="value_label_2",
                        style={'text-align': 'center', 'font-size': 30,
                               'text-decoration': 'bold', 'margin-right': '20%'})
            ], className="pretty_container", style={'width': '31%'}),
            html.Div([
                html.P(id='title_label_3'),
                html.H6(id="value_label_3",
                        style={'text-align': 'center', 'font-size': 30,
                               'text-decoration': 'bold', 'margin-right': '20%'})
            ], className="pretty_container", style={'width': '31%'}),
        ], className='row', style={'margin-top': '0.5%', 'margin-bottom': '0.5%'}),

        html.Div([  # second row
            html.Div([
                html.P(
                    'Filtering:',
                    style={'font-size': 20, 'text-decoration': 'bold'}
                ),
                html.P('Date range: ', style={'margin-left': 15, 'margin-top': 5, 'text-decoration': 'bold'}),
                dcc.DatePickerRange(
                    id='date_picker',
                    min_date_allowed=date(2021, 1, 1),
                    max_date_allowed=date(2021, 12, 31),
                    initial_visible_month=date(2021, 5, 1),
                    start_date=date(2021, 5, 1),
                    end_date=date(2021, 5, 31)
                ),
                html.P('Shift: ', style={'margin-left': 15, 'margin-top': 10, 'text-decoration': 'bold'}),
                dcc.Checklist(id='filter-checklist', options=[
                    {'label': '      Morning', 'value': 'MS'},
                    {'label': '      Afternoon', 'value': 'AS'},
                    {'label': '      Night', 'value': 'NS'},
                ], value=['MS', 'AS', 'NS'], labelStyle={'display': 'block'}),
                html.Div([
                    html.P('Recipe: ', style={'margin-left': 15, 'margin-top': 10, 'text-decoration': 'bold'}),
                    dcc.Dropdown(
                        id='filter_dropdown',
                        options=recipes_options,
                        multi=False,
                        value='All',
                        className="dcc_control"
                    )
                ]),
                html.Div([
                     html.P(id='extra_filter_p', style={'margin-left': 15, 'margin-top': 10, 'text-decoration': 'bold'}),
                     dcc.Dropdown(
                         id='extra_filter_dropdown',
                         multi=False,
                         value='All',
                         className="dcc_control"
                     )], id='extra_filter', hidden=False)

            ], className='pretty_container', style={'width': '31%'}),
            html.Div([
                dcc.Graph(id='main_graph', style={'height': 360, 'display': 'inline-block', 'width': '100%'},
                          figure={'layout': {'paper_bgcolor': '#F9F9F9', 'plot_bgcolor': '#F9F9F9'}},
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
                                style={'margin_bottom': '1%', 'text-decoration': 'underline'}),
                        dcc.Graph(id='pool_graph{}'.format(4*i+j+1), style={'height': 150, 'width': '100%'},
                                  config={'displayModeBar': False, 'showTips': False}),
                        html.H4('Processed bundles: ', id='label1_pool{}'.format(4*i+j+1)),
                        html.H5('Processed surface: ', id='label2_pool{}'.format(4*i+j+1)),
                        html.H5('Processed weight: ', id='label3_pool{}'.format(4*i+j+1))
                    ], className='col-3')
                for j in range(4)], className='row col-12')
            for i in range(4)], id='div3_pool', hidden=False, className='row col-12')

        ], className='row', style={'margin-top': '1%', 'margin-bottom': '1%'})
    ], className='pretty_container col-10', style={}),

    html.Div([], className='col-1')  # column for right margin

], className='row', style={'margin-top': '1%', 'margin-bottom': '1%'})

header = html.Div([
    html.Div([], className='col-2'),  # Same as img width, allowing to have the title centrally aligned
    html.Div([
        html.H1(
            children='Performance Dashboard',
            style={'textAlign': 'center'}
        )
    ], className='col-8'),
    html.Div([
        html.Img(
                src='/assets/images/kupner-logo.jpeg',
                height='43 px',
                width='auto')
        ], className='col-2', style={'align-items': 'center',
                                     'padding-top': '0.65%',
                                     'height': 'auto'})
    ],
    className='row',
    style={'height': '1%', 'backgroundColor': '#E7E7E7'}
)
