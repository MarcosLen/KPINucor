RECIPES = ['Normal_1', 'Normal_2', 'Stripping_20', 'Stripping_40', 'Stripping_60', 'Stripping_80',
           'Without_Degrease', 'Only_Flux', '5_inch', 'Flux_and_go', 'New_Drgreaser', 'Degrease_5']
recipes_options = [
    {'label': 'All', 'value': 'All', 'disabled': False},
    {'label': 'Normal_1', 'value': 'Normal_1', 'disabled': False},
    {'label': 'Normal_2', 'value': 'Normal_2', 'disabled': True},
    {'label': 'Stripping_20', 'value': 'Stripping_20', 'disabled': True},
    {'label': 'Stripping_40', 'value': 'Stripping_40', 'disabled': True},
    {'label': 'Stripping_60', 'value': 'Stripping_60', 'disabled': True},
    {'label': 'Stripping_80', 'value': 'Stripping_80', 'disabled': True},
    {'label': 'Without_Degrease', 'value': 'Without_Degrease', 'disabled': False},
    {'label': 'Only_Flux', 'value': 'Only_Flux', 'disabled': False},
    {'label': '5_inch', 'value': '5_inch', 'disabled': True},
    {'label': 'Flux_and_go', 'value': 'Flux_and_go', 'disabled': True},
    {'label': 'New_Drgreaser', 'value': 'New_Drgreaser', 'disabled': True},
    {'label': 'Degrease_5', 'value': 'Degrease_5', 'disabled': True}
]

pool_dict = [{'label': 'All', 'value': 'All'},
             {'label': 'Stripping 1', 'value': 'S1'},
             {'label': 'Stripping 2', 'value': 'S2'},
             {'label': 'Degrease 1', 'value': 'D1'},
             {'label': 'Degrease 2', 'value': 'D2'},
             {'label': 'Degrease Rinse 1', 'value': 'DR1'},
             {'label': 'Degrease Rinse 2', 'value': 'DR2'},
             {'label': 'Pickling 2', 'value': 'P2'},
             {'label': 'Pickling 3', 'value': 'P3'},
             {'label': 'Pickling 4', 'value': 'P4'},
             {'label': 'Pickling 5', 'value': 'P5'},
             {'label': 'Pickling 6', 'value': 'P6'},
             {'label': 'Pickling 7', 'value': 'P7'},
             {'label': 'Pickling 8', 'value': 'P8'},
             {'label': 'Pickling Rinse 1', 'value': 'PR1'},
             {'label': 'Pickling Rinse 2', 'value': 'PR2'},
             {'label': 'Flux', 'value': 'F'}
             ]

trolley_dict = [{'label': 'All', 'value': 'All'},
                {'label': 'Trolley_1', 'value': 'T1'},
                {'label': 'Trolley_2', 'value': 'T2'},
                {'label': 'Trolley_3', 'value': 'T3'},
                {'label': 'Trolley_4', 'value': 'T4'}]

Normal_1_steps = {
    'Degrease': 12,
    'Degrease_rinse': 0,
    'Pickling': 25,
    'Pickling_rinse': 0,
    'Flux': 60,
    'Exit': 0
}

Without_Degrease_steps = {
    'Pickling': 20,
    'Pickling_rinse': 0,
    'Flux': 0,
    'Exit': 0
}

Only_Flux_steps = {
    'Flux': 10,
    'Exit': 0
}

possible_failures = ['Unknown', 'Trolley Failure', 'Bundle Lost', 'Engine Failure', 'Missing Sensor']
