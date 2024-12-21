from dash import Dash
from components.main import main_layout
from dash import Output, Input
from callbacks_functions.control_panel_callback import control_panel_input_list, masking_control_panel_callbacks
import pandas as pd
from configurations.functions import get_dash_callback_args
from components.num_time_components import num_time_row, cat_row
from configurations.configurations import anomaly_col, datetime_col, num_cols, cat_cols, id_col
from callbacks_functions.num_time_callback import make_num_time_figs, make_cat_time_figs
from components.cat_num_components import cat_num_row
from io import StringIO
from callbacks_functions.cat_num_callbacks import make_cat_num_figs


app = Dash()
app.layout = main_layout
server = app.server

control_input_list = control_panel_input_list()
control_out_list = [Output(component_id='intermediate-value', component_property='data')]


@app.callback(control_out_list, control_input_list)
def control_panel_callbacks(*args):
    from configurations.configurations import df
    temp_df = masking_control_panel_callbacks(df=df, temp_args=args)
    return [temp_df.to_json(date_format='iso', orient='split')]


num_time_output, num_time_input = get_dash_callback_args(num_time_row)
num_time_input.append(Input('intermediate-value', 'data'))


@app.callback(num_time_output, num_time_input)
def update_graph(*args):
    if len(args) > 1:
        dff = pd.read_json(StringIO(args[-1]), orient='split')

        time_fig = make_num_time_figs(df=dff, num_cols=args[0], date_col=datetime_col,
                                      anomaly_col=anomaly_col, cat_col=args[2], date_agg_col=args[1])
        return time_fig


cat_time_output, cat_time_input = get_dash_callback_args(cat_row)
cat_time_input.append(Input('intermediate-value', 'data'))


@app.callback(cat_time_output, cat_time_input)
def update_cat_time_graph(*args):
    if len(args) > 1:
        dff = pd.read_json(StringIO(args[-1]), orient='split')
        fig_list = make_cat_time_figs(df=dff, date_col=datetime_col,
                                      date_agg_col=args[1],
                                      anomaly_col=anomaly_col,
                                      cat_col=args[0],
                                      id_col=id_col)
        return fig_list


cat_row_output, cat_row_input = get_dash_callback_args(cat_num_row)
cat_row_input.append(Input('intermediate-value', 'data'))


@app.callback(cat_row_output, cat_row_input)
def update_cat_num_graph(*args):
    if len(args) > 1:
        dff = pd.read_json(StringIO(args[-1]), orient='split')
        figs = make_cat_num_figs(df=dff, selected_cat_col=args[1], num_cols=args[0], cat_cols=cat_cols,
                                 anomaly_col=anomaly_col)
        return figs


if __name__ == '__main__':
    app.run(debug=True)
