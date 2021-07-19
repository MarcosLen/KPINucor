import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from controls import pool_dict, trolley_dict, RECIPES
from assets.Data_gen import pool_temp, pool_uses, failures, recipes_used, real_production, dist_data_n
import datetime
from collections import deque

app.config.suppress_callback_exceptions = True
X = deque(maxlen=20)
X.append(0)
Y0 = deque(maxlen=20)
Y0.append(0)
Y1 = deque(maxlen=20)
Y1.append(0)
Y2 = deque(maxlen=20)
Y2.append(0)
Y3 = deque(maxlen=20)
Y3.append(0)

graph_std_layout = {'margin': {'l': 25, 'r': 5, 't': 10, 'b': 0}, 'showlegend': True,
                    'legend': {'itemclick': False, 'itemdoubleclick': False},
                    'xaxis': {'tickangle': 45}}


@app.callback([Output('extra_filter_p', 'children'),
               Output('extra_filter_dropdown', 'options'),
               Output('extra_filter', 'hidden')],
              Input('tab_selector', 'active_tab'))
def extra_filter(tab):
    if tab == 'tab2':
        return ['Filter by pool', pool_dict, False]
    else:
        return ['', [], True]


@app.callback([Output('div3_trolley', 'hidden'),
               Output('div3_pool', 'hidden')],
              Input('tab_selector', 'active_tab'))
def show_3div(tab):
    if tab in ['tab1', 'tab4']:
        return [False, True]
    elif tab == 'tab2':
        return [True, False]
    return [True, True]


@app.callback([Output('title_label_1', 'children'),
               Output('title_label_2', 'children'),
               Output('title_label_3', 'children')],
              [Input('tab_selector', 'active_tab')])
def title_labels(value):
    if value == 'tab1':
        return 'Completed Bundles', 'Usage Time', 'Failures'
    elif value == 'tab2':
        return 'Accumulated Surface', 'Total Usage Time', 'Exceeded Time per step'
    elif value == 'tab3':
        return 'Total Production', 'Moving Time per process', 'Settle Time per process'
    elif value == 'tab4':
        return 'Total Travelled', 'Energy implied', 'Raising distance'
    return 'error', 'error', 'error'


@app.callback([Output('value_label_1', 'children'),
               Output('value_label_2', 'children'),
               Output('value_label_3', 'children')],
              [Input('tab_selector', 'active_tab'),
               Input('main_graph', 'figure')])
def title_values(tab, figure):
    if tab == 'tab1':
        return '{}'.format(sum(recipes_used['Times'])), '62%', '{}'.format(sum(failures['Times']))
    elif tab == 'tab2':
        return '42.325 m{}\u00b2'.format(''), '1971.6 hs', '1.2 min'
    elif tab == 'tab3':
        return '{}'.format(sum(recipes_used['Times'])), '12.4 min', '62.1 min'
    elif tab == 'tab4':
        data = figure['data']
        energy = sum([x * y for i in range(len(data)) for x, y in enumerate(data[i]['y'])])
        dist = sum([len(data[i]['x']) for i in range(len(data))])
        raising_times = sum([True if (data[i]['y'][j] == 0 and data[i]['y'][j] != data[i]['y'][j + 1]) else False
                             for i in range(len(data)) for j in range(len(data[i]['y']) - 1)])
        return '{} km'.format(dist), '{:.2f} W'.format(energy), '{:.2f} m'.format(raising_times*2*8.35)
    return 'error', 'error', 'error'


@app.callback([Output('main_graph', 'figure'),
               Output('main_graph_title', 'children')],
              [Input('tab_selector', 'active_tab'),
               Input('extra_filter_dropdown', 'value'),
               Input('interval_comp', 'n_intervals')])
def draw_main_graph(tab, extra_filt, n):
    if tab == 'tab1':
        x = pool_uses['Pool']
        y = pool_uses['Time']
        data = [{'x': x, 'y': y, 'type': 'bar'}]
        fig = go.Figure(data=data)
        fig.update_layout(graph_std_layout)
        fig.update_layout({'showlegend': False})
        return fig, 'Time usage by pool'

    elif tab == 'tab2':
        x = pool_uses['Pool']
        y = pool_uses['Time']
        y2 = pool_uses['Nottime']
        data = [{'x': x, 'y': y, 'type': 'bar', 'name': 'Used Time'},
                {'x': x, 'y': y2, 'type': 'bar', 'name': 'Not Used Time', 'opacity': 0.6, 'marker': {'color': '#7a7e85'}}]
        fig = go.Figure(data=data)
        fig.update_layout(graph_std_layout)
        fig.update_layout({'barmode': 'stack'})
        return fig, 'Time usage by pool'

    elif tab == 'tab3':
        # data = real_production[(real_production['Day'] > datetime.datetime.strptime(start_date, '%Y-%m-%d')) &
        #                        (real_production['Day'] < datetime.datetime.strptime(end_date, '%Y-%m-%d'))]
        data = [{'x': recipes_used['Recipe'], 'y': recipes_used['Times'], 'type': 'bar'}]
        fig = go.Figure(data=data)
        fig.update_layout(graph_std_layout)
        fig.update_layout({'showlegend': False})
        fig.update_xaxes(tickangle=45)
        return fig, 'Recipes Produced'

    elif tab == 'tab4':
        fig = go.Figure()
        X.append(X[-1]+1)
        Y0.append(dist_data_n(Y0[-1]))
        Y1.append(dist_data_n(Y1[-1]))
        Y2.append(dist_data_n(Y2[-1]))
        Y3.append(dist_data_n(Y3[-1]))

        fig.add_trace(go.Scatter({'x': list(X), 'y': list(Y0), 'name': 'Trolley_1', 'line_shape': 'hv'}))
        fig.add_trace(go.Scatter({'x': list(X), 'y': list(Y1), 'name': 'Trolley_2', 'line_shape': 'hv'}))
        fig.add_trace(go.Scatter({'x': list(X), 'y': list(Y2), 'name': 'Trolley_3', 'line_shape': 'hv'}))
        fig.add_trace(go.Scatter({'x': list(X), 'y': list(Y3), 'name': 'Trolley_4', 'line_shape': 'hv'}))
        fig.update_layout(graph_std_layout)
        fig.update_layout({'hovermode': 'x', 'hoverdistance': 100, 'spikedistance': 1000})
        fig.update_xaxes({'title': 'distance (km)', 'type': 'linear', 'tickmode': 'linear',
                          'tick0': 0, 'dtick': 1, 'showticklabels': True, 'tickangle': 0, 'range': [min(X), max(X)]})
        fig.update_yaxes({'title': 'weight (kg)', 'type': 'linear', 'range': [0, 3]})
        return fig, 'Energy (weight/km)'

    fig = go.Figure()
    fig.update_layout(graph_std_layout)
    return fig, 'Error'


@app.callback([Output('small_graph_1', 'figure'),
               Output('sm_graph_1_title', 'children')],
              [Input('tab_selector', 'active_tab')])
def draw_small_graph_1(tab):
    if tab == 'tab1':
        data = []
        total = 0
        for i in pool_uses.index:
            time = pool_uses['Time'][i]
            name = pool_uses['Pool'][i]
            total = total + time
            data.append([name, time])
        datatot = pd.DataFrame(data, columns=['Pool', 'Time'])
        fig = px.pie(datatot, values='Time', names='Pool')
        fig.update_layout(graph_std_layout)
        return fig, 'Pool usage ratio'

    if tab == 'tab4':
        x = [x for x in range(11)]
        data = [{'x': x, 'y': [0, 0, 1, 2, 0, 0, 0.6, 1.2, 1.8, 0, 0], 'mode': 'lines', 'name': 'Trolley_1'},
                {'x': x, 'y': [0, 0.5, 1, 1.5, 0, 4, 0, 1.2, 2.4, 3.6, 0], 'mode': 'lines', 'name': 'Trolley_2'},
                {'x': x, 'y': [0, 0, 0, 0, 0, 0, 0, 0.3, 0.6, 0, 0], 'mode': 'lines', 'name': 'Trolley_3'},
                {'x': x, 'y': [0, 2, 4, 0, 0, 1.5, 3, 4.5, 0, 0, 0], 'mode': 'lines', 'name': 'Trolley_4'}]

        data1 = sum(data[0]['y'])
        data2 = sum(data[1]['y'])
        data3 = sum(data[2]['y'])
        data4 = sum(data[3]['y'])
        datatot = pd.DataFrame([['Trolley 1', data1], ['Trolley 2', data2], ['Trolley 3', data3], ['Trolley 4', data4]],
                               columns=['Trolley', 'Value'])
        fig = px.pie(datatot, values='Value', color='Trolley', names='Trolley')
        fig.update_layout(graph_std_layout)
        return fig, 'Usage ratio'
    return {'data': [],
            'layout': {}}, ''


@app.callback([Output('small_graph_2', 'figure'),
              Output('sm_graph_2_title', 'children')],
              [Input('tab_selector', 'active_tab')])
def draw_main_graph(tab):
    if tab == 'tab1':
        data = [{'x': failures['Failure'], 'y': failures['Times'], 'type': 'bar'}]
        fig = go.Figure(data=data)
        fig.update_layout(graph_std_layout)
        fig.update_layout({'showlegend': False})
        return fig, 'Failures'
    elif tab == 'tab4':
        x = ['Trolley 1', 'Trolley 2', 'Trolley 3', 'Trolley 4']
        data = [go.Bar(name='Auto', x=x, y=[75, 85, 25, 50]),
                go.Bar(name='Manual', x=x, y=[20, 15, 50, 25]),
                go.Bar(name='Emergencia', x=x, y=[5, 0, 25, 25])]
        fig = go.Figure(data=data)
        fig.update_layout(barmode='group')
        fig.update_layout(graph_std_layout)
        return fig, 'Usage mode'
    else:
        return {'data': [],
                'layout': {}}, ''


@app.callback([Output('small_graph_3', 'figure'),
              Output('sm_graph_3_title', 'children')],
              [Input('tab_selector', 'active_tab')])
def graph_small_graph_3(tab):
    if tab == 'tab1':
        data = [{'x': recipes_used['Recipe'], 'y': recipes_used['Times'], 'type': 'bar'}]
        fig = go.Figure(data=data)
        fig.update_layout(graph_std_layout)
        fig.update_layout({'showlegend': False})
        fig.update_xaxes(tickangle=45)
        return fig, 'Recipes Completed'
    elif tab == 'tab4':
        data = [{'Auto': 75, 'Manual': 20, 'Emergency': 5},
                {'Auto': 85, 'Manual': 15, 'Emergency': 0},
                {'Auto': 25, 'Manual': 50, 'Emergency': 25},
                {'Auto': 50, 'Manual': 25, 'Emergency': 25}]
        data1 = ['Auto', sum(data[i]['Auto'] for i in range(len(data)))]
        data2 = ['Manual', sum(data[i]['Manual'] for i in range(len(data)))]
        data3 = ['Emergency', sum(data[i]['Emergency'] for i in range(len(data)))]

        datatot = pd.DataFrame([data1, data2, data3], columns=['Mode', 'Value'])
        fig = px.pie(datatot, values='Value', color='Mode', names='Mode')
        fig.update_layout(graph_std_layout)
        return fig, 'Usage mode ratio'
    return {'data': [],
            'layout': {}}, ''


@app.callback([Output('pool_graph{}'.format(i+1), 'figure') for i in range(len(pool_temp.columns))],
              Input('tab_selector', 'active_tab'))
def pool_graphs(tab):
    this_graph_layout = graph_std_layout.copy()
    this_graph_layout['showlegend'] = False
    this_graph_layout['xaxis'] = {'tickangle': 0}
    if tab == 'tab2':
        ret = []
        for col in pool_temp.columns:
            x = pool_temp[col].index
            y = pool_temp[col].values
            data = [{'x': x, 'y': y, 'name': col, 'mode': 'lines'}]
            fig = go.Figure(data=data)
            fig.update_layout(this_graph_layout)
            ret.append(fig)
        return ret
    return [{'data': [], 'layout': graph_std_layout} for _ in range(len(pool_temp.columns))]


@app.callback([Output('label{}_pool{}'.format(j+1, i+1), 'children')
               for i in range(len(pool_uses.index)) for j in range(3)],
              Input('tab_selector', 'active_tab'))
def pool_graphs(tab):
    data = []
    if tab == 'tab2':
        for i in pool_uses.index:
            data.append('{}'.format(pool_uses['Units'][i]))
            data.append('{:.2f}'.format(pool_uses['Surface'][i]))
            data.append('{:.2f}'.format(pool_uses['Weight'][i]))
        return data
    return ['' for _ in range(len(pool_uses.index)) for _ in range(3)]
