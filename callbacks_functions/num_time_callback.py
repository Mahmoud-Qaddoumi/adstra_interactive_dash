import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import Figure

from configurations.configurations import datetime_col


def make_num_time_figs(df: pd.DataFrame, num_cols: list, date_col: str, anomaly_col: str, cat_agg_col: str = None,
                       date_agg_col: str = None) -> list[Figure]:
    df[date_col] = pd.to_datetime(df[date_col])
    if cat_agg_col is None or cat_agg_col == 'No Aggregation':
        if date_agg_col is None or date_agg_col == 'Actual Data':
            mode = 'markers'
        else:
            df = group_dataframe(df, datetime_col=date_col, cols_to_sum=num_cols, anomaly_col=anomaly_col,
                                 grouping=date_agg_col, cat_col=None)
            mode = 'lines'
    else:
        if date_agg_col is None or date_agg_col == 'Actual Data':
            df[date_col] = df[date_col].dt.date
            df = group_dataframe(df, datetime_col=date_col, cols_to_sum=num_cols, anomaly_col=anomaly_col,
                                 grouping='day', cat_col=cat_agg_col)
            mode = 'markers'
        else:
            df = group_dataframe(df, datetime_col=date_col, cols_to_sum=num_cols, anomaly_col=anomaly_col,
                                 grouping=date_agg_col, cat_col=cat_agg_col)
            mode = 'markers'
    hover_template = "".join([f"{str(col)}:%{df[col]}: <br>" for col in df.columns])

    time_traces = [go.Scatter(x=df[date_col], y=df[col], mode=mode, name=col) for col in num_cols]
    time_layout = go.Layout(title="Time Series - Numeric  ", legend=dict(orientation="h"), margin=dict(r=0),
                            )
    time_fig = go.Figure(data=time_traces, layout=time_layout)
    anomalies_indexes = df[df[anomaly_col] == True].index
    for anomaly in anomalies_indexes:
        time_fig.add_vline(x=df.at[anomaly, date_col], line_dash='dash', line_color='red')
    violin_traces = [go.Violin(y=df[col], side='positive', x0='Total', showlegend=False, box=dict(visible=True),
                               meanline=dict(visible=True), name=col) for col in num_cols]
    violin_layout = go.Layout(title="Distribution of Numerical features", legend=None, yaxis={'side': 'right'},
                              margin=dict(l=0))
    violin_fig = go.Figure(data=violin_traces, layout=violin_layout)
    return [time_fig, violin_fig]

def group_dataframe(df: pd.DataFrame, datetime_col: str, cols_to_sum: list, anomaly_col: str, grouping: str,
                    cat_col: str = None,aggregation_fun:str='sum') -> pd.DataFrame:
    df[datetime_col] = pd.to_datetime(df[datetime_col])
    group_funcs = {'day': lambda x: x.dt.floor('D'),
                   'week': lambda x: x.dt.to_period('W').dt.to_timestamp(),
                   'month': lambda x: x.dt.to_period('M').dt.to_timestamp()}
    df[datetime_col] = group_funcs[grouping](df[datetime_col])
    group_cols = [datetime_col]
    if cat_col:
        group_cols.append(cat_col)

    agg_dict = {col: aggregation_fun for col in cols_to_sum + [anomaly_col]}
    result = df.groupby(group_cols).agg(agg_dict).reset_index()
    return result

def make_cat_time_figs(df:pd.DataFrame, cat_col:str, date_col:str, anomaly_col:str,
                       date_agg_col: str = None) -> list[Figure]:
    df = group_dataframe(df=df, datetime_col=date_col, cols_to_sum=[anomaly_col], anomaly_col=anomaly_col,
                         grouping=date_agg_col, cat_col=cat_col, aggregation_fun='count')
    traces = [go.Bar(x=df.loc[df[cat_col]==temp_class, date_col],
                     y=df.loc[df[cat_col]==temp_class, anomaly_col],
                     name=temp_class) for temp_class in df[cat_col].unique()]
    layout = go.Layout(title="Time Series - Categorical Features", barmode='group', legend=dict(orientation="h"), )
    fig = go.Figure(data=traces, layout=layout)
    return [fig]




