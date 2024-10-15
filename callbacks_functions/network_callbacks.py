import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import Figure
import plotly.express as px
import numpy as np

def make_network_callbacks(df, left_col, right_col, color_col, anomaly_col):
    right_entities = list(df[right_col].value_counts().index)[:10]
    left_entities =  list(df[left_col].value_counts().index)[:10]
    color_entities =  list(df[color_col].value_counts().index)
    df =df[(df[left_col].isin(left_entities)) & (df[right_col].isin(right_entities))]
    x = df.groupby(by=[left_col, right_col, color_col],as_index=False)[anomaly_col].count()
    # x = df.groupby(by=[left_col, right_col, color_col],as_index=False).agg(count=(anomaly_col,'count'),
    #                                                                        sum=)
    # traces = [go.Scatter(x='right', y=right_entities, mode='markers'),
    #           go.Scatter(x='left', y=left_entities, mode='markers'),]
    color_map = px.colors.qualitative.Plotly[:len(color_entities)]
    cat_to_color = dict(zip(color_entities, color_map))
    # new_colors = np.where(df[anomaly_col], x[color_col].map(cat_to_color))

    traces_1 =  [go.Scatter(x=[left_col, right_col],
                            y=[row[left_col], row[right_col]],
                            line=dict(width=2,
                                      color=cat_to_color[row[color_col]]),
                            marker=dict(size=20),
                            mode='lines+markers',name=f'{row[left_col]} - {row[right_col]}',
                            showlegend=False) for i,row in x.iterrows()]
    layout = go.Layout(title='connections',height=1600,)
    fig = go.Figure(data=traces_1, layout=layout)
    return [fig]

