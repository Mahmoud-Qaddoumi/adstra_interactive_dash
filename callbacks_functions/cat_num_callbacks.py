import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import Figure
import plotly.express as px
import numpy as np

def make_cat_num_figs(df:pd.DataFrame, selected_cat_col:str,num_cols:list, cat_cols:list,
                      anomaly_col:str) -> list[Figure]:
    categories = df[selected_cat_col].unique()
    color_map = px.colors.qualitative.Plotly[:len(categories)]
    cat_to_color = dict(zip(categories, color_map))
    new_colors = np.where(df[anomaly_col], 'black', df[selected_cat_col].map(cat_to_color))
    new_symbols = np.where(df[anomaly_col], 'square', 'circle')
    traces = go.Splom(dimensions=[dict(label=col, values=df[col]) for col in num_cols],
                      showupperhalf=False,
                      text=df[selected_cat_col],
                      marker=dict(size=8,
                                  color=new_colors,
                                  symbol=new_symbols,
                                  showscale=False, line_color="white",
                                  line_width=0.5),
                      diagonal=dict(visible=False))
    layout = go.Layout(title="PCA with Anomalies Highlighted",
                       hoversubplots='axis',
                       # width=1600,
                       height=1600,
                       hovermode="x",
                       )
    fig = go.Figure(data=traces, layout=layout)
    return [fig]
