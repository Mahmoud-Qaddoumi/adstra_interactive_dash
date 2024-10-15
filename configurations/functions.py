from datetime import datetime
import pandas as pd
from collections import deque
from dash.html.Div import Div
from dash import Output, Input

def date_time_configurations_maker(df: pd.DataFrame, datetime_col: str = None) -> dict:
    if datetime_col is None:
        result = {}
    else:

        result = {'disabled': False,
                  'width': '100%',
                  'first_date': df[datetime_col].min(),
                  'last_date': df[datetime_col].max(),
                  'id': 'date_time_component_id'}
    return result


def dropdown_configurations_maker(df: pd.DataFrame, categorical_cols=None) -> list:
    if categorical_cols is None:
        categorical_cols = []
    result = [dict(label=f'Select {col}:', id=f"{col}_component_id", options=df[col].unique(),
                   value=None) for col in categorical_cols]
    return result


def radio_configuration_maker(df: pd.DataFrame, bool_cols: list) -> list:
    if bool_cols:
        result = []
        for col in bool_cols:
            result.append(dict(label=f'{col}:', id=f"{col}_component_id", options=df[col].unique()))
    else:
        result = []
    return result


def slider_configurations_maker(df: pd.DataFrame, num_cols: list) -> list:
    if num_cols:
        result = []
        for col in num_cols:
            min_value, max_value = df[col].min(), df[col].max()
            result.append(dict(label=f'Select {col}:', id=f"{col}_component_id",
                               min_value=min_value, max_value=max_value,))
    else:
        result = []
    return result

def get_dash_callback_args(component:Div):
    outputs = []
    inputs = []
    queue = deque([component])
    while queue:
        current = queue.popleft()
        if hasattr(current, 'id'):
            component_type = type(current).__name__
            if component_type == 'Graph':
                outputs.append(Output(component_id=current.id, component_property='figure'))
            elif component_type in ['Checklist', 'RadioItems', 'Dropdown', 'Slider', 'RangeSlider', 'Input']:
                inputs.append(Input(component_id=current.id, component_property='value'))
        if hasattr(current, 'children'):
            if isinstance(current.children, list):
                queue.extend(current.children)
            else:
                queue.append(current.children)
    return outputs, inputs