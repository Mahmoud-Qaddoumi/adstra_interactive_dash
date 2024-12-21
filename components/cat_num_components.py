from dash import html, dcc
from configurations.configurations import num_cols, cat_cols

if len(num_cols) >= 1:
    selector_label = html.P(children="Numeric Column(s): ",
                            style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
    num_selector = dcc.Checklist(id='cat_numerical_cols_id', options=num_cols, value=num_cols, inline=True,
                                 style={'display': 'flex', "margin-left": "0", "margin-right": "0", 'width': '100%'})
    num_selector_div = html.Div(children=[selector_label, num_selector],
                                style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
    if len(cat_cols) > 1:
        cat_selector = html.P(children="Categorical Feature Aggregation: ",
                                  style={'textAlign': 'left', "margin-left": "0", "margin-right": "0", 'width': '100%'})
        cat_options = dcc.Dropdown(id='cat_num_options_id', options=cat_cols,
                                       value=cat_cols[0], multi=False, searchable=False,
                                       style={'width': '90%', "margin-left": "0", "margin-right": "0", })
        cat_selector_div = html.Div(children=[cat_selector, cat_options],
                                    style={'textAlign': 'Left', 'verticalAlign': 'top', 'width': '100%'})
        selector_row = html.Div(children=[num_selector_div, cat_selector_div],
                                style={'width': '100%', 'display': 'flex'}) #, "border": "2px black solid"
        cat_num_row = html.Div(children=[selector_row,
                                         html.Div(dcc.Graph(id='pca_figure', animate=False), style=dict(width='100%'))],
                               style={'width': '100%'})
    elif len(cat_cols) == 1:
        selector_row = html.Div(children=[num_selector_div],
                                style={'width': '100%', 'display': 'flex'})
        cat_num_row = html.Div(children=[selector_row,
                                         html.Div(dcc.Graph(id='pca_figure', animate=False), style=dict(width='100%'))],
                               style={'width': '100%'})
    else:
        cat_num_row = html.Div(children=[html.P(children="No Categorical Columns Selected",
                                                 style={'width': '100%', 'textAlign': 'center'})],
                                style={'width': '100%'})
else:
    cat_num_row = html.Div(children=[html.P(children="No Numeric Columns Selected",
                                            style={'width': '100%', 'textAlign': 'center'})],
                           style={'width': '100%'})




