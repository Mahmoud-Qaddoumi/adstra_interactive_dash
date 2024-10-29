from dash import html, dcc
from configurations.configurations import numeric_cols, categorical_cols

if len(numeric_cols) > 1:
    selector_label = html.P(children="Numeric Column(s): ",
                            style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
    categorical_cols_with_no_agg = categorical_cols + ['No Aggregation']
    num_selector = dcc.Checklist(id='numerical_cols_id', options=numeric_cols, value=numeric_cols, inline=True,
                                 style={'display': 'flex', "margin-left": "0", "margin-right": "0", 'width': '100%'})
    date_agg_selector = html.P(children="Date Aggregation: ",
                               style={'textAlign': 'Left', 'verticalAlign': 'center', "margin-left": "0",
                                      "margin-right": "0", 'width': '100%'})

    date_agg_options = dcc.Dropdown(id='date_num_agg_options_id', options=['Actual Data', 'day', 'week', 'month'],
                                    value=['Actual Data'], multi=False, searchable=False,
                                    style={"margin-left": "0", "margin-right": "0", 'width': '90%'})
    cat_agg_selector = html.P(children="Categorical Feature Aggregation: ",
                              style={'textAlign': 'left', "margin-left": "0", "margin-right": "0", 'width': '100%'})
    cat_agg_options = dcc.Dropdown(id='cat_num_agg_options_id', options=categorical_cols_with_no_agg,
                                   value=['No Aggregation'], multi=False, searchable=False,
                                   style={'width': '90%', "margin-left": "0", "margin-right": "0", })
    date_agg_div = html.Div(children=[date_agg_selector, date_agg_options], style={'width': '25%'})
    cat_agg_div = html.Div(children=[cat_agg_selector, cat_agg_options], style={'width': '25%'})
    columns_selection_div = html.Div(children=[selector_label, num_selector], style={'width': '50%'})
    selector_row = html.Div(children=[columns_selection_div, date_agg_div, cat_agg_div],
                            style={'width': '100%', 'display': 'flex'})

    time_graph = dcc.Graph(id='time_graph_id', animate=False,
                           style={'width': '100%', "margin-left": "0", "margin-right": "0", 'margin': '0px'})
    # box_graph = dcc.Graph(id='box_graph_id', animate=False,
    #                       style={'width': '20%', "margin-left": "0", "margin-right": "0", 'margin': '0px',
    #                              'padding': '0px'})
    graphs_row = html.Div(children=[time_graph],
                          style={'width': '100%', 'display': 'flex', "margin-left": "0", "margin-right": "0",
                                 'margin': '0px'})
    num_time_row = html.Div(children=[selector_row, graphs_row], style={'width': '100%'})
else:
    num_time_row = html.Div(children=[html.P(children="No Numeric Columns Selected",
                                             style={'width': '100%', 'textAlign': 'center'})],
                            style={'width': '100%'})

if len(categorical_cols) > 1:
    selector_label = html.P(children="Categorical Column: ",
                            style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '10%'})
    cat_selector = dcc.Dropdown(id='categorical_cols_id', options=categorical_cols, value=categorical_cols[0],
                                multi=False, searchable=False, style={'width': '35%'})
    agg_selector = html.P(children="Select Aggregation: ", style={'width': '15%', 'textAlign': 'Right'})
    agg_options = dcc.Dropdown(id='cat_agg_options_id', options=['day', 'month', 'week'], value=['day', 'month', 'week'][0],
                               multi=False, searchable=False, style={'width': '35%'})
    cat_time_graph = dcc.Graph(id='cat_time_graph_id', animate=False, style={'width': '100%'})
    cat_selector_row = html.Div(children=[selector_label, cat_selector, agg_selector, agg_options],
                                style={'width': '100%', 'display': 'flex'})
    cat_row = html.Div(children=[cat_selector_row, cat_time_graph], style={'width': '100%'})
else:
    cat_row = html.Div(children=[html.P(children="No Categorical Columns Selected",
                                        style={'width': '100%', 'textAlign': 'center'})],
                       style={'width': '100%'})

dash_time_div = html.Div(children=[num_time_row, cat_row], style={'width': '100%'})
