from dash import html, dcc
from configurations.configurations import numeric_cols, categorical_cols

selector_label_1 = html.P(children="First Column: ",
                        style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
cat_1_options = dcc.Dropdown(id='network_first_options_id', options=categorical_cols,
                           value=categorical_cols[0], multi=False, searchable=False,
                           style={'width': '90%', "margin-left": "0", "margin-right": "0", })
selector_label_2 = html.P(children="Second Column: ",
                        style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
cat_2_options = dcc.Dropdown(id='network_second_options_id', options=categorical_cols,
                           value=categorical_cols[1], multi=False, searchable=False,
                           style={'width': '90%', "margin-left": "0", "margin-right": "0", })
selector_label_circle_size = html.P(children="Circle Size Column: ",
                                    style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
circle_size_options = dcc.Dropdown(id='circle_size_options_id', options=numeric_cols,
                                   value=numeric_cols[0], multi=False, searchable=False,
                                   style={'width': '90%', "margin-left": "0", "margin-right": "0", })
selector_label_circle_color = html.P(children="Circle Color Column: ",
                                    style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
circle_color_options = dcc.Dropdown(id='circle_color_options_id', options=numeric_cols,
                                   value=numeric_cols[1], multi=False, searchable=False,
                                   style={'width': '90%', "margin-left": "0", "margin-right": "0", })
selector_label_line_color = html.P(children="Connections Color Column: ",
                                    style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
line_color_options = dcc.Dropdown(id='line_color_options_id', options=numeric_cols,
                                   value=numeric_cols[2], multi=False, searchable=False,
                                   style={'width': '90%', "margin-left": "0", "margin-right": "0", })
selector_label_line_size = html.P(children="Connections Size Column: ",
                                    style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
line_size_options = dcc.Dropdown(id='line_size_options_id', options=numeric_cols,
                                   value=numeric_cols[3], multi=False, searchable=False,
                                   style={'width': '90%', "margin-left": "0", "margin-right": "0", })


selector_1_div = html.Div(children=[selector_label_1, cat_1_options],
                            style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '16.6%'})
selector_2_div = html.Div(children=[selector_label_2, cat_2_options],
                            style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '16.6%'})
selector_circle_size_div = html.Div(children=[selector_label_circle_size, circle_size_options],
                              style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '16.6%'})
selector_circle_color_div = html.Div(children=[selector_label_circle_color, circle_color_options],
                              style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '16.6%'})
selector_line_color_div = html.Div(children=[selector_label_line_color, line_color_options],
                              style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '16.6%'})
selector_line_size_div = html.Div(children=[selector_label_line_size, line_size_options],
                              style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '16.6%'})

selector_row = html.Div(children=[selector_1_div, selector_2_div, selector_circle_size_div, selector_circle_color_div,
                                  selector_line_color_div, selector_line_size_div],
                        style={'width': '100%', 'display': 'flex'})  # , "border": "2px black solid"

network_row = html.Div(children=[selector_row,
                                 html.Div(dcc.Graph(id='network_figure', animate=False), style=dict(width='100%')),
                                 ],
                       style={'width': '100%'})

