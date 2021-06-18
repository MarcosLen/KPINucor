import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from controls import pool_dict, trolley_dict, RECIPES
from assets.Data_gen import pool_temp, pool_uses, failures, recipes_used, real_production
import datetime

app.config.suppress_callback_exceptions = True


graph_std_layout = {'paper_bgcolor': '#F9F9F9', 'plot_bgcolor': '#F9F9F9',
                    'margin': {'l': 35, 'r': 10, 't': 35, 'b': 30}, 'showlegend': True,
                    'legend': {'itemclick': False, 'itemdoubleclick': False},
                    'xaxis': {'tickangle': 45}}


@app.callback([Output('extra_filter_p', 'children'),
               Output('extra_filter_dropdown', 'options'),
               Output('extra_filter', 'hidden')],
              Input('tab_selector', 'value'))
def extra_filter(tab):
    if tab == 'tab1':
        return ['', [], True]
    if tab == 'tab2':
        return ['Filter by pool', pool_dict, False]
    elif tab == 'tab4':
        return ['Filter by Trolley', trolley_dict, False]
    return ['', [], True]


@app.callback([Output('div3_trolley', 'hidden'),
               Output('div3_pool', 'hidden')],
              Input('tab_selector', 'value'))
def show_3div(tab):
    if tab in ['tab1', 'tab4']:
        return [False, True]
    elif tab == 'tab2':
        return [True, False]
    return [True, True]


@app.callback([Output('title_label_1', 'children'),
               Output('title_label_2', 'children'),
               Output('title_label_3', 'children')],
              [Input('tab_selector', 'value')])
def title_labels(value):
    if value == 'tab1':
        return 'Completed Bundles', 'Usage Time', 'Failures'
    elif value == 'tab2':
        return 'Accumulated Surface', 'Total Usage Time', 'Exceeded Time'
    elif value == 'tab3':
        return 'Total Production', 'Moving Time (prom)', 'Settle Time (prom)'
    elif value == 'tab4':
        return 'Total Travelled', 'Energy implied', 'Raising distance'
    return 'error', 'error', 'error'


@app.callback([Output('value_label_1', 'children'),
               Output('value_label_2', 'children'),
               Output('value_label_3', 'children')],
              [Input('tab_selector', 'value'),
               Input('main_graph', 'figure')])
def title_values(tab, figure):
    if tab == 'tab1':
        return '{}'.format(sum(recipes_used['Times'])), '62%', '{}'.format(sum(failures['Times']))
    elif tab == 'tab2':
        return '42.325 m{}\u00b2'.format(''), '1971.6 hs', '23.1 hs'
    elif tab == 'tab3':
        return '{}'.format(sum(recipes_used['Times'])), '12.4 min/proc', '62.1 min/proc'
    elif tab == 'tab4':
        data = figure['data']
        energy = sum([x * y for i in range(len(data)) for x, y in enumerate(data[i]['y'])])
        dist = sum([len(data[i]['x']) for i in range(len(data))])
        raising_times = sum([True if (data[i]['y'][j] == 0 and data[i]['y'][j] != data[i]['y'][j + 1]) else False
                             for i in range(len(data)) for j in range(len(data[i]['y']) - 1)])
        return '{} km'.format(dist), '{} W'.format(energy), '{} m'.format(raising_times*2*8.35)
    return 'error', 'error', 'error'


@app.callback(Output('main_graph', 'figure'),
              [Input('tab_selector', 'value'),
               Input('extra_filter_dropdown', 'value')])
def draw_main_graph(tab, extra_filt):
    if tab == 'tab1':
        x = pool_uses['Pool']
        y = pool_uses['Time']
        data = [{'x': x, 'y': y, 'type': 'bar'}]
        return {
            'data': data,
            'layout': {'title': 'Time usage by pool',
                       'paper_bgcolor': '#F9F9F9',
                       'plot_bgcolor': '#F9F9F9'}
        }

    elif tab == 'tab2':
        data = []
        for col in pool_temp:
            x = pool_temp[col].index
            y = pool_temp[col].values
            data.append({'x': x, 'y': y, 'name': col, 'mode': 'lines'})
        if extra_filt != 'All':
            data = [data[i] for i in range(len(pool_dict)) if pool_dict[i]['value'] == extra_filt]
        return {
            'data': data,
            'layout': {'showlegend': True,
                       'title': 'Pool Temperature',
                       'paper_bgcolor': '#F9F9F9',
                       'plot_bgcolor': '#F9F9F9'}
        }
    elif tab == 'tab3':
        # data = real_production[(real_production['Day'] > datetime.datetime.strptime(start_date, '%Y-%m-%d')) &
        #                        (real_production['Day'] < datetime.datetime.strptime(end_date, '%Y-%m-%d'))]
        data = [{'x': recipes_used['Recipe'], 'y': recipes_used['Times'], 'type': 'bar'}]
        fig = go.Figure(data=data)
        fig.update_layout(graph_std_layout)
        fig.update_layout({'title': 'Recipes Produced', 'showlegend': False})
        fig.update_xaxes(tickangle=45)
        return fig

    elif tab == 'tab4':
        x = [x for x in range(11)]
        data = [{'x': x, 'y': [0, 0, 1, 2, 0, 0, 0.6, 1.2, 1.8, 0, 0], 'mode': 'lines', 'name': 'Trolley_1',
                 'line': {'color': 'blue'}},
                {'x': x, 'y': [0, 0.5, 1, 1.5, 0, 4, 0, 1.2, 2.4, 3.6, 0], 'mode': 'lines', 'name': 'Trolley_2',
                 'line': {'color': 'orange'}},
                {'x': x, 'y': [0, 0, 0, 0, 0, 0, 0, 0.3, 0.6, 0, 0], 'mode': 'lines', 'name': 'Trolley_3',
                 'line': {'color': 'green'}},
                {'x': x, 'y': [0, 2, 4, 0, 0, 1.5, 3, 4.5, 0, 0, 0], 'mode': 'lines', 'name': 'Trolley_4',
                 'line': {'color': 'red'}}]

        if extra_filt == 'T1':
            data = [data[0]]
        elif extra_filt == 'T2':
            data = [data[1]]
        elif extra_filt == 'T3':
            data = [data[2]]
        elif extra_filt == 'T4':
            data = [data[3]]

        return {
            'data': data,
            'layout': {
                'xaxis': {
                    'title': 'distance (km)',
                    'type': 'linear',
                    'tickmode': 'linear',
                    'tick0': 0,
                    'dtick': 1,
                    'showticklabels': True,
                },
                'yaxis': {
                    'title': 'weight (kg)',
                    'type': 'linear',
                },
                'showlegend': True,
                'title': 'Work (weight/km)',
                'paper_bgcolor': '#F9F9F9',
                'plot_bgcolor': '#F9F9F9',
                'hovermode': 'x',
                'hoverdistance': 100,
                'spikedistance': 1000,
                'itemclick': False,
                'itemdoubleclick': False
            }}
    return {
        'data': [],
        'layout': {'paper_bgcolor': '#F9F9F9',
                   'plot_bgcolor': '#F9F9F9'}
    }


@app.callback(Output('small_graph_1', 'figure'),
              [Input('tab_selector', 'value')])
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
        fig = px.pie(datatot, title='Pool usage ratio', values='Time', names='Pool')
        fig.update_layout(graph_std_layout)
        return fig

    if tab == 'tab4':
        x = [x for x in range(11)]
        data = [{'x': x, 'y': [0, 0, 1, 2, 0, 0, 0.6, 1.2, 1.8, 0, 0], 'mode': 'lines', 'name': 'Trolley_1',
                 'line': {'color': 'blue'}},
                {'x': x, 'y': [0, 0.5, 1, 1.5, 0, 4, 0, 1.2, 2.4, 3.6, 0], 'mode': 'lines', 'name': 'Trolley_2',
                 'line': {'color': 'orange'}},
                {'x': x, 'y': [0, 0, 0, 0, 0, 0, 0, 0.3, 0.6, 0, 0], 'mode': 'lines', 'name': 'Trolley_3',
                 'line': {'color': 'green'}},
                {'x': x, 'y': [0, 2, 4, 0, 0, 1.5, 3, 4.5, 0, 0, 0], 'mode': 'lines', 'name': 'Trolley_4',
                 'line': {'color': 'red'}}]

        data1 = sum(data[0]['y'])
        data2 = sum(data[1]['y'])
        data3 = sum(data[2]['y'])
        data4 = sum(data[3]['y'])
        datatot = pd.DataFrame([['Trolley 1', data1], ['Trolley 2', data2], ['Trolley 3', data3], ['Trolley 4', data4]],
                               columns=['Trolley', 'Value'])
        fig = px.pie(datatot, title='Usage ratio', values='Value', color='Trolley',


                     names='Trolley', color_discrete_map={'Trolley 1': 'blue', 'Trolley 2': 'orange',
                                                          'Trolley 3': 'green', 'Trolley 4': 'red'})
        fig.update_layout(graph_std_layout)
        return fig
    return {'data': [],
            'layout': {}}


@app.callback(Output('small_graph_2', 'figure'),
              [Input('tab_selector', 'value')])
def draw_main_graph(tab):
    if tab == 'tab1':
        data = [{'x': failures['Failure'], 'y': failures['Times'], 'type': 'bar'}]
        fig = go.Figure(data=data)
        fig.update_layout(graph_std_layout)
        fig.update_layout({'title': 'Failures', 'showlegend': False})
        return fig
    elif tab == 'tab4':
        x = ['Trolley 1', 'Trolley 2', 'Trolley 3', 'Trolley 4']
        data = [go.Bar(name='Auto', x=x, y=[75, 85, 25, 50], marker={'color': 'blue'}),
                go.Bar(name='Manual', x=x, y=[20, 15, 50, 25], marker={'color': 'red'}),
                go.Bar(name='Emergencia', x=x, y=[5, 0, 25, 25], marker={'color': 'green'})]
        fig = go.Figure(data=data)
        fig.update_layout(barmode='group')
        fig.update_layout(graph_std_layout)
        fig.update_layout({'title': 'Usage mode'})
        return fig
    else:
        return {'data': [],
                'layout': {}}


@app.callback(Output('small_graph_3', 'figure'),
              [Input('tab_selector', 'value')])
def graph_small_graph_3(tab):
    if tab == 'tab1':
        data = [{'x': recipes_used['Recipe'], 'y': recipes_used['Times'], 'type': 'bar'}]
        fig = go.Figure(data=data)
        fig.update_layout(graph_std_layout)
        fig.update_layout({'title': 'Recipes Completed', 'showlegend': False})
        fig.update_xaxes(tickangle=45)
        return fig
    elif tab == 'tab4':
        data = [{'Auto': 75, 'Manual': 20, 'Emergency': 5},
                {'Auto': 85, 'Manual': 15, 'Emergency': 0},
                {'Auto': 25, 'Manual': 50, 'Emergency': 25},
                {'Auto': 50, 'Manual': 25, 'Emergency': 25}]
        data1 = ['Auto', sum(data[i]['Auto'] for i in range(len(data)))]
        data2 = ['Manual', sum(data[i]['Manual'] for i in range(len(data)))]
        data3 = ['Emergency', sum(data[i]['Emergency'] for i in range(len(data)))]

        datatot = pd.DataFrame([data1, data2, data3], columns=['Mode', 'Value'])
        fig = px.pie(datatot, title='Usage mode ratio', values='Value', color='Mode', names='Mode',
                     color_discrete_map={'Auto': 'blue', 'Manual': 'red', 'Emergency': 'green'})
        fig.update_layout(graph_std_layout)
        return fig
    return {'data': [],
            'layout': {}}


@app.callback([Output('pool_graph{}'.format(i+1), 'figure') for i in range(len(pool_temp.columns))],
              Input('tab_selector', 'value'))
def pool_graphs(tab):
    this_graph_layout = graph_std_layout.copy()
    this_graph_layout['showlegend'] = False
    this_graph_layout['xaxis'] = {'tickangle': 0}
    if tab == 'tab2':
        fig = []
        for col in pool_temp.columns:
            x = pool_temp[col].index
            y = pool_temp[col].values
            data = [{'x': x, 'y': y, 'name': col, 'mode': 'lines'}]
            dic = {'data': data, 'layout': this_graph_layout}
            fig.append(dic)
        return fig
    return [{'data': [], 'layout': graph_std_layout} for _ in range(len(pool_temp.columns))]


@app.callback([Output('label{}_pool{}'.format(j+1, i+1), 'children')
               for i in range(len(pool_uses.index)) for j in range(3)],
              Input('tab_selector', 'value'))
def pool_graphs(tab):
    data = []
    if tab == 'tab2':
        for i in pool_uses.index:
            data1 = 'Processed bundles: {}'.format(pool_uses['Units'][i])
            data2 = 'Processed surface: {:.2f}'.format(pool_uses['Surface'][i])
            data3 = 'Processed weight: {:.2f}'.format(pool_uses['Weight'][i])
            data.append(data1)
            data.append(data2)
            data.append(data3)
        return data
    return ['' for _ in range(len(pool_uses.index)) for _ in range(3)]
