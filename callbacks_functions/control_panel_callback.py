from dash import Input, State
from configurations.configurations import categorical_configurations, numeric_configurations, bool_configurations, \
    datetime_col, num_cols, cat_cols, bool_cols, target_col
import pandas as pd


def control_panel_input_list(cat_config: dict = categorical_configurations,
                             num_config: dict = numeric_configurations,
                             bool_config: dict = bool_configurations) -> list:
    input_list = [Input(component_id='apply_filter_button', component_property='n_clicks'),
                  State(component_id='date_time_component_id', component_property='start_date'),
                  State(component_id='date_time_component_id', component_property='end_date')]
    for cat in cat_config:
        input_list.append(State(component_id=cat['id'], component_property='value'))

    for num_temp in num_config:
        input_list.append(State(component_id=num_temp['id'], component_property='value'))

    for bool_temp in bool_config:
        input_list.append(State(component_id=bool_temp['id'], component_property='value'))
    return input_list


def masking_control_panel_callbacks(df: pd.DataFrame, temp_args: tuple, cat_list: list = cat_cols,
                                    num_list: list = num_cols, bool_list: list = bool_cols) -> pd.DataFrame:
    mask = (df[datetime_col] >= pd.to_datetime(temp_args[1])) & (df[datetime_col] <= pd.to_datetime(temp_args[2]))
    for i, bool_col in enumerate(bool_list):
        args_index = i + 3 + len(cat_list) + len(num_list)
        mask = (df[bool_col].isin(temp_args[args_index])) & mask

    for i, cat in enumerate(cat_list):
        if temp_args[i + 3]:
            if cat == target_col:
                mask = (df[cat] == temp_args[i + 3]) & mask
            else:
                mask = (df[cat].isin(temp_args[i + 3])) & mask

    for i, num_col in enumerate(num_list):
        args_index = i + 3 + len(cat_list)
        mask = (df[num_col] >= temp_args[args_index][0]) & (df[num_col] <= temp_args[args_index][1]) & mask

    return df[mask]
