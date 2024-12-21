from datetime import datetime
import pandas as pd
from collections import deque
from dash.html.Div import Div
from dash import Output, Input
from sqlalchemy import create_engine, inspect
from urllib.parse import quote_plus

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


def dropdown_configurations_maker(df: pd.DataFrame, categorical_cols=None, target_col:str=None) -> list:
    if categorical_cols is None:
        categorical_cols = []
    result = [dict(label=f'Select {col}:',
                   id=f"{col}_component_id",
                   options=df[col].unique(),
                   value=None) for col in categorical_cols]
    return result


def radio_configuration_maker(df: pd.DataFrame, bool_cols: list) -> list:
    if bool_cols:
        result = []
        for col in bool_cols:
            result.append(dict(label=f'{col}:',
                               id=f"{col}_component_id",
                               options=df[col].unique()))
    else:
        result = []
    return result


def slider_configurations_maker(df: pd.DataFrame, num_cols: list) -> list:
    if num_cols:
        result = []
        for col in num_cols:
            min_value, max_value = df[col].min(), df[col].max()
            result.append(dict(label=f'Select {col}:',
                               id=f"{col}_component_id",
                               min_value=min_value,
                               max_value=max_value,))
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



def make_query(table_name: str,
               id_column: str = None,
               date_column: str = None,
               categorical_columns: list = None,
               numerical_columns: list = None,
               boolean_columns: list = None,
               start_date: str = None,
               end_date: str = None,
               limit: int = 100,
               custom_where: str = None) -> str:
    # Initialize empty lists if None provided
    categorical_columns = categorical_columns or []
    numerical_columns = numerical_columns or []
    boolean_columns = boolean_columns or []

    # Build column list
    columns = []
    if id_column:
        columns.append(id_column)
    if date_column:
        columns.append(date_column)

    # Add other columns
    columns.extend(categorical_columns)
    columns.extend(numerical_columns)
    columns.extend(boolean_columns)
    # Remove duplicates while preserving order
    columns = list(dict.fromkeys(columns))
    # Build a base query
    if limit > 0:
        query = f"SELECT TOP {limit} {', '.join(columns)} FROM {table_name}"
    else:
        query = f"SELECT {', '.join(columns)} FROM {table_name}"
    # Build WHERE clause
    where_conditions = []
    # Add date range condition if both dates are provided
    if date_column and (start_date or end_date):
        if start_date and end_date:
            where_conditions.append(
                f"CAST({date_column} AS DATE) BETWEEN '{format_date(start_date)}' AND '{format_date(end_date)}'")
        elif start_date:
            where_conditions.append(f"CAST({date_column} AS DATE) >= '{format_date(start_date)}'")
        elif end_date:
            where_conditions.append(f"CAST({date_column} AS DATE) <= '{format_date(end_date)}'")
    # Add custom WHERE conditions if provided
    if custom_where:
        where_conditions.append(f"({custom_where})")
    # Combine WHERE conditions
    if where_conditions:
        query += " WHERE " + " AND ".join(where_conditions)
    return query


def format_date(date_str: str) -> str:
    if not date_str:
        return None
    try:
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except:
        raise ValueError(f"Invalid date format: {date_str}")

def get_exact_query(query, db_details):
    engine = get_sqlalchemy_sqlserver_connection(db_details=db_details)
    df = pd.read_sql(query, engine)
    return df

def get_sqlalchemy_sqlserver_connection(db_details):
    params = quote_plus(db_details)
    conn_str = f"mssql+pyodbc:///?odbc_connect={params}"
    engine = create_engine(conn_str)
    return engine
