import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import Figure
import plotly.express as px


def make_num_time_figs(df: pd.DataFrame, date_col: str, num_cols: list, anomaly_col: str,
                       cat_col: str = 'No Aggregation',
                       date_agg_func: str = 'sum', date_agg_col: str = 'Actual Data') -> list[Figure]:
    # ToDo: add selection for aggregation function so the user can select "sum", "Average" ...etc. for categorical agg.
    if cat_col is None or cat_col == 'No Aggregation':
        if date_agg_col is None or date_agg_col == 'Actual Data':
            time_fig_markers = 'markers'
        else:
            time_fig_markers = 'lines'
            df = group_dataframe(df, datetime_col=date_col, cols_to_agg=num_cols, anomaly_col=anomaly_col,
                                 grouping=date_agg_col, cat_col=None, aggregation_fun=date_agg_func)
    else:
        if date_agg_col is None or date_agg_col == 'Actual Data':
            time_fig_markers = 'lines'
            df = group_dataframe(df, datetime_col=date_col, cols_to_agg=num_cols, anomaly_col=anomaly_col,
                                 grouping='day', cat_col=cat_col, aggregation_fun=date_agg_func)
        else:
            time_fig_markers = 'markers'
            df = group_dataframe(df, datetime_col=date_col, cols_to_agg=num_cols, anomaly_col=anomaly_col,
                                 grouping=date_agg_col, cat_col=cat_col, aggregation_fun=date_agg_func)

    # Create dynamic hover template based on available columns
    hover_template = "<b>Date:</b> %{x}<br>"
    exclude_cols = [date_col]  # List of columns to exclude from hover

    # Add all available numeric columns to hover template
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        if col not in exclude_cols:
            hover_template += f"<b>{col}:</b> %{{customdata[{list(df.columns).index(col)}]:,.2f}}<br>"

    # Add all categorical columns to hover template
    for col in df.select_dtypes(include=['object', 'category']).columns:
        if col not in exclude_cols:
            hover_template += f"<b>{col}:</b> %{{customdata[{list(df.columns).index(col)}]}}<br>"

    # Add boolean columns to hover template
    for col in df.select_dtypes(include=['bool']).columns:
        if col not in exclude_cols:
            hover_template += f"<b>{col}:</b> %{{customdata[{list(df.columns).index(col)}]}}<br>"

    hover_template += "<extra></extra>"  # Remove secondary box

    colors = px.colors.qualitative.Plotly
    time_traces, violin_traces = [], []
    for i, col in enumerate(num_cols):
        color = colors[i % len(colors)]  # Cycle through colors if more columns than colors
        # Time series trace
        time_traces.append(go.Scatter(x=df[date_col], y=df[col], xaxis='x1', yaxis='y',
                                      name=col, legendgroup=col,
                                      mode=time_fig_markers, marker=dict(color=color,size=10), line=dict(color=color),
                                      customdata=df.values, hovertemplate=hover_template,
                                      hoverlabel=dict(bgcolor='white', font_size=12, font_family="Arial")))
        # Violin trace
        violin_traces.append(go.Violin(y=df[col], side='positive', x0='Total', xaxis='x2', yaxis='y',
                                       showlegend=False, legendgroup=col,
                                       box=dict(visible=True), meanline=dict(visible=True),
                                       name=col, line_color=color, fillcolor=color, marker_color=color))
    anomalies_indexes = df[df[anomaly_col] == True].index
    anomaly_traces = []
    y_min = df[num_cols].min().min()
    y_max = df[num_cols].max().max()

    for anomaly in anomalies_indexes:
        # Vertical line for scatter plot
        anomaly_traces.append(go.Scatter(x=[df.at[anomaly, date_col], df.at[anomaly, date_col]],
                                         y=[y_min, y_max],
                                         mode='lines',
                                         line=dict(color='black', dash='dash'),
                                         name='Anomaly',
                                         legendgroup='anomaly',
                                         showlegend=False,
                                         hoverinfo='skip',
                                         xaxis='x1'))
        # Horizontal line for violin plot
        anomaly_traces.append(go.Scatter(x=['Total', 'Max'],  # This will span the width of the violin plot
                                         y=[df.at[anomaly, num_cols[0]], df.at[anomaly, num_cols[0]]],
                                         mode='lines',
                                         line=dict(color='black', dash='dash'),
                                         name='Anomaly',
                                         legendgroup='anomaly',
                                         showlegend=False,
                                         hoverinfo='skip',
                                         xaxis='x2'))
    if anomaly_traces:  # Only add if there are anomalies
        anomaly_traces[0].showlegend = True
    traces = time_traces + violin_traces + anomaly_traces

    layout = go.Layout(title="Time Series - Numeric", grid=dict(rows=1, columns=2), legend=dict(orientation="h"),
                       xaxis1=dict(domain=[0, 0.74]), xaxis2=dict(domain=[0.75, 1]))
    result_fig = go.Figure(data=traces, layout=layout)
    return [result_fig]


def group_dataframe(df: pd.DataFrame,
                    datetime_col: str,  # datetime column to make group by
                    cols_to_agg: list,
                    anomaly_col: str,
                    grouping: str,
                    cat_col: str = None,
                    aggregation_fun: str = 'sum') -> pd.DataFrame:
    df[datetime_col] = pd.to_datetime(df[datetime_col])
    group_funcs = {'day': lambda x: x.dt.floor('D'),
                   'week': lambda x: x.dt.to_period('W').dt.to_timestamp(),
                   'month': lambda x: x.dt.to_period('M').dt.to_timestamp()}
    df[datetime_col] = group_funcs[grouping](df[datetime_col])
    group_cols = [datetime_col]
    if cat_col:
        group_cols.append(cat_col)
    agg_dict = {col: aggregation_fun for col in cols_to_agg + [anomaly_col]}
    result = df.groupby(group_cols).agg(agg_dict).reset_index()
    if aggregation_fun != 'sum':
        result.loc[result[anomaly_col] > 0, anomaly_col] = 1
    return result


def make_cat_time_figs(df: pd.DataFrame, id_col: str, cat_col: str, date_col: str, anomaly_col: str,
                       date_agg_col: str = None) -> list[Figure]:
    df.rename(columns={'is_anomaly': 'counts'}, inplace=True)
    anomaly_col = 'counts'
    df = df.drop_duplicates(subset=[id_col], keep='first')
    df[cat_col] = df[cat_col].astype('str')
    normal_df = df[df[anomaly_col] == False]
    normal_df.loc[:, anomaly_col] = True
    df = df[df[anomaly_col] == True]
    df.to_pickle('test.pkl')
    df = group_dataframe(df=df, datetime_col=date_col, cols_to_agg=[anomaly_col], anomaly_col=anomaly_col,
                         grouping=date_agg_col, cat_col=cat_col, aggregation_fun='sum')
    normal_df = group_dataframe(df=normal_df, datetime_col=date_col, cols_to_agg=[anomaly_col], anomaly_col=anomaly_col,
                                grouping=date_agg_col, cat_col=cat_col, aggregation_fun='sum')
    df.to_pickle('after_grouping.pkl')

    colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)', 'rgb(148, 103, 189)',
              'rgb(140, 86, 75)', 'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)', 'rgb(23, 190, 207)',
              'rgb(141, 211, 199)', 'rgb(255, 255, 179)', 'rgb(190, 186, 218)', 'rgb(251, 128, 114)',
              'rgb(128, 177, 211)', 'rgb(253, 180, 98)', 'rgb(179, 222, 105)', 'rgb(252, 205, 229)',
              'rgb(217, 217, 217)', 'rgb(188, 128, 189)']
    hover_template = "<b>Date:</b> %{x}<br>"
    exclude_cols = [date_col]

    # Create hover template for all columns except date
    for col in df.columns:
        if col not in exclude_cols:
            hover_template += f"<b>{col}:</b> %{{customdata[{list(df.columns).index(col)}]}}<br>"
    hover_template += "<extra></extra>"

    # Prepare customdata for both dataframes
    normal_df['customdata'] = normal_df.values.tolist()
    df['customdata'] = df.values.tolist()
    traces = []
    for i, temp_class in enumerate(df[cat_col].unique()):
        color = colors[i]
        traces.append(go.Bar(x=normal_df.loc[normal_df[cat_col] == temp_class, date_col],
                             y=normal_df.loc[normal_df[cat_col] == temp_class, anomaly_col],
                             marker_color=color,
                             customdata=normal_df.loc[normal_df[cat_col] == temp_class].values.tolist(),
                             hovertemplate=hover_template,
                             name=f"{temp_class} - Normal"))
        traces.append(go.Bar(x=df.loc[df[cat_col] == temp_class, date_col],
                             y=df.loc[df[cat_col] == temp_class, anomaly_col],
                             name=f"{temp_class} - Anomaly",
                             customdata=df.loc[df[cat_col] == temp_class].values.tolist(),
                             hovertemplate=hover_template,
                             marker_color=color,
                             marker_line_color='black',
                             marker_line_width=4, ))
    layout = go.Layout(title="Time Series - Categorical Features",
                       barmode='group',
                       legend=dict(orientation="h"),
                       barcornerradius=5, )
    fig = go.Figure(data=traces, layout=layout)
    return [fig]
