from dash import html, dcc
from .filters_components import control_panel
from configurations.configurations import dashboard_name
from .num_time_components import dash_time_div
from .cat_num_components import cat_num_row
from .network_graph import network_row
temp_fig = dcc.Graph(id='test_id', style={'width': '80%'})
header_row = html.H1(children=dashboard_name, style={'textAlign': 'center', 'width': '100%'})

figs_div = html.Div(children=[dash_time_div, cat_num_row, network_row], style={ 'width': '100%'})
main_row = html.Div(children=[figs_div, control_panel], style={'display': 'flex', 'width': '100%'})
main_layout = html.Div(children=[header_row,
                                 main_row,
                                 dcc.Store(id='intermediate-value')],
                       style={'width': '100%'})
