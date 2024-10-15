from dash import html, dcc
from configurations.configurations import (categorical_configurations, bool_configurations, time_configurations,
                                           numeric_configurations)

if len(time_configurations.keys()) > 0:
    date_picker = dcc.DatePickerRange(id=time_configurations['id'],
                                      min_date_allowed=time_configurations['first_date'],
                                      max_date_allowed=time_configurations['last_date'],
                                      start_date=time_configurations['first_date'],
                                      end_date=time_configurations['last_date'],
                                      first_day_of_week=0,
                                      show_outside_days=False,
                                      minimum_nights=0,
                                      style={'width': '100%'},
                                      disabled=time_configurations['disabled'])
else:
    date_picker = html.P(children="No Time Column", style={'textAlign': 'center', 'width': '100%'})

if len(categorical_configurations) > 0:
    categorical_list = [element for category in categorical_configurations for element in
                        (html.P(children=category['label'], style={'width': '100%', 'textAlign': 'Left'}),
                         dcc.Dropdown(id=category['id'], value=category['value'], options=category['options'],
                                      multi=True, style={'width': '100%'}))]
else:
    categorical_list = html.P(children="No categorical Columns", style={'textAlign': 'center', 'width': '100%'})

if len(bool_configurations) > 0:

    bool_list = [html.Div(children=[html.P(children=bool_case['label'], style={'width': '50%', 'textAlign': 'Left'}),
                                    dcc.Checklist(id=bool_case['id'], inline=True,
                                                  value=[option for option in bool_case['options']],
                                                  style={'width': '50%'},
                                                  options=[{'label': str(option), 'value': option} for option in
                                                           bool_case['options']])],
                          style={'width': '100%', 'display': 'flex'}) for bool_case in bool_configurations]
else:
    bool_list = html.P(children="No Bool Columns", style={'textAlign': 'center', 'width': '100%'})

if len(numeric_configurations) > 0:
    num_list = [html.Div(children=[html.P(children=[numeric['label']], style={'width': '100%', 'textAlign': 'Left'}),
                                   dcc.RangeSlider(id=numeric['id'],
                                                   min=numeric['min_value'],
                                                   max=numeric['max_value'],
                                                   marks=None,
                                                   value=[numeric['min_value'], numeric['max_value']],
                                                   tooltip={"placement": "bottom", "always_visible": True},
                                                   step=1)]) for numeric in numeric_configurations]
else:
    num_list = html.P(children="No Numerical Columns", style={'textAlign': 'center', 'width': '100%'})

apply_button = html.Button(children='Apply Filters', id='apply_filter_button', type='Danger',
                           style={'width': '100%', 'background-color': '#DC3545', 'color': 'black', 'padding': '3px',
                                  "borderRadius": "10px"})

control_panel = html.Div(children=[html.H3(children='Date Column:',
                                           style={'textAlign': 'left', 'width': '100%'}),
                                   html.Div(children=date_picker,
                                            style={'width': '100%'}),
                                   html.H3(children='Categorical columns:',
                                           style={'textAlign': 'left', 'width': '100%'}),
                                   html.Div(children=categorical_list,
                                            style={'width': '100%'}),
                                   html.H3(children='Boolean columns:',
                                           style={'textAlign': 'left', 'width': '100%'}),
                                   html.Div(children=bool_list,
                                            style={'width': '100%'}),
                                   html.H3(children='Numeric Columns:',
                                           style={'textAlign': 'left', 'width': '100%'}),
                                   html.Div(children=num_list,
                                            style={'width': '100%'}),
                                   apply_button],
                         style={'width': '20%'})
