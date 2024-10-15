from dash import html, dcc
from configurations.configurations import numeric_cols, categorical_cols

selector_label_1 = html.P(children="Left Column: ",
                        style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
cat_1_options = dcc.Dropdown(id='network_first_options_id', options=categorical_cols,
                           value=categorical_cols[0], multi=False, searchable=False,
                           style={'width': '90%', "margin-left": "0", "margin-right": "0", })
selector_label_2 = html.P(children="Right Column: ",
                        style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
cat_2_options = dcc.Dropdown(id='network_second_options_id', options=categorical_cols,
                           value=categorical_cols[1], multi=False, searchable=False,
                           style={'width': '90%', "margin-left": "0", "margin-right": "0", })
selector_label_color = html.P(children="Color Column: ",
                        style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
cat_color_options = dcc.Dropdown(id='network_color_options_id', options=categorical_cols,
                           value=categorical_cols[2], multi=False, searchable=False,
                           style={'width': '90%', "margin-left": "0", "margin-right": "0", })
selector_1_div = html.Div(children=[selector_label_1, cat_1_options],
                            style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '30%'})
selector_2_div = html.Div(children=[selector_label_2, cat_2_options],
                            style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '30%'})
selector_color_div = html.Div(children=[selector_label_color, cat_color_options],
                            style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '30%'})

selector_row = html.Div(children=[selector_1_div, selector_2_div, selector_color_div],
                        style={'width': '100%', 'display': 'flex'})  # , "border": "2px black solid"
network_row = html.Div(children=[selector_row,
                                 html.Div(dcc.Graph(id='network_figure', animate=False), style=dict(width='100%'))],
                       style={'width': '100%'})

