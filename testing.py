import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import List, Tuple, Dict, Optional
from collections import defaultdict


def calculate_network_metrics(G):
    """
    Calculate various network metrics for the graph
    """
    metrics = {'degree_centrality': nx.degree_centrality(G),
               'betweenness_centrality': nx.betweenness_centrality(G),
               'closeness_centrality': nx.closeness_centrality(G),
               'eigenvector_centrality': nx.eigenvector_centrality_numpy(G),
               'clustering_coefficient': nx.clustering(G)}
    return metrics


def identify_anomalies(G, metrics, threshold=0.95):
    """
    Identify anomalous nodes based on network metrics
    """
    anomalies = defaultdict(list)
    for metric_name, metric_values in metrics.items():
        values = np.array(list(metric_values.values()))
        threshold_value = np.percentile(values, threshold * 100)
        anomalous_nodes = [node for node, value in metric_values.items() if value > threshold_value]
        anomalies[metric_name] = anomalous_nodes
    return anomalies


def make_network_callbacks(df, left_col, right_col, color_col, anomaly_col):
    """
    Enhanced network callback function with anomaly detection and additional metrics
    """
    # Create color mapping
    color_entities = list(df[color_col].unique())
    color_map = px.colors.qualitative.Plotly[:len(color_entities)]
    cat_to_color = dict(zip(color_entities, color_map))

    # Create node categories mapping
    node_categories = {}
    node_anomalies = {}

    for _, row in df.iterrows():
        # Map categories
        node_categories[row[left_col]] = row[color_col]
        node_categories[row[right_col]] = row[color_col]

        # Map anomalies if present
        if anomaly_col:
            node_anomalies[row[left_col]] = row.get(anomaly_col, False)
            node_anomalies[row[right_col]] = row.get(anomaly_col, False)

    # Create graph
    G = nx.Graph()
    G.add_edges_from(zip(df[left_col], df[right_col]))

    # Calculate network metrics
    metrics = calculate_network_metrics(G)
    anomalies = identify_anomalies(G, metrics)

    # Create the network visualization
    fig = create_network_graph(edges=list(zip(df[left_col], df[right_col])),
                               node_color_mapping=cat_to_color,
                               node_categories=node_categories,
                               node_anomalies=node_anomalies,
                               network_metrics=metrics,
                               anomalies=anomalies)
    return [fig]


def create_network_graph(edges: List[Tuple[str, str]],
                         node_colors: Optional[Dict[str, str]] = None,
                         node_color_mapping: Optional[Dict[str, str]] = None,
                         node_categories: Optional[Dict[str, str]] = None,
                         node_anomalies: Optional[Dict[str, bool]] = None,
                         network_metrics: Optional[Dict[str, Dict]] = None,
                         anomalies: Optional[Dict[str, List]] = None):
    """
    Enhanced network graph creation with anomaly highlighting and metric visualization
    """
    # Create network graph
    G = nx.Graph()
    G.add_edges_from(edges)

    # Calculate layout
    pos = nx.spring_layout(G, k=1 / np.sqrt(len(G.nodes())), iterations=50)

    # Calculate node sizes based on degree centrality and anomaly status
    degrees = dict(G.degree())
    base_size = 10
    node_sizes = {}
    for node, degree in degrees.items():
        size = (degree + 1) * base_size
        # Increase size for anomalous nodes
        if node_anomalies and node_anomalies.get(node):
            size *= 1.5
        node_sizes[node] = size

    # Handle node colors
    if node_color_mapping and node_categories:
        node_colors = {node: node_color_mapping.get(node_categories.get(node, ''), '#888888')
                       for node in G.nodes()}
    elif node_colors is None:
        max_degree = max(degrees.values())
        node_colors = {node: f'rgb({int(255 * degree / max_degree)},100,200)'
                       for node, degree in degrees.items()}

    # Create edge traces with curves
    edge_traces = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        # Calculate curve control points
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        curve_x = [x0, mid_x + (y1 - y0) * 0.2, x1]
        curve_y = [y0, mid_y - (x1 - x0) * 0.2, y1]

        # Create edge trace
        edge_trace = go.Scatter(x=curve_x,
                                y=curve_y,
                                mode='lines',
                                line=dict(width=0.5, color='#888'),
                                hoverinfo='none')
        edge_traces.append(edge_trace)

    # Create node trace with enhanced hover information
    node_x, node_y = [], []
    node_colors_list = []
    node_sizes_list = []
    node_text = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_colors_list.append(node_colors.get(node, '#888888'))
        node_sizes_list.append(node_sizes[node])

        # Create detailed hover text
        hover_text = [f'Node: {node}']
        if node_categories:
            hover_text.append(f'Category: {node_categories.get(node, "")}')
        hover_text.append(f'Connections: {degrees[node]}')

        # Add metrics to hover text
        if network_metrics:
            for metric_name, metric_values in network_metrics.items():
                value = metric_values.get(node, 0)
                hover_text.append(f'{metric_name}: {value:.3f}')

        # Add anomaly information
        if node_anomalies and node_anomalies.get(node):
            hover_text.append('⚠️ Anomaly detected')

        node_text.append('<br>'.join(hover_text))

    # Create node trace
    node_trace = go.Scatter(x=node_x,
                            y=node_y,
                            mode='markers',
                            hoverinfo='text',
                            text=node_text,
                            marker=dict(showscale=False,
                                        color=node_colors_list,
                                        size=node_sizes_list,
                                        line=dict(width=1, color='#888'),
                                        symbol=['circle' if not node_anomalies.get(node, False) else 'star' for node in
                                                G.nodes()] if node_anomalies else 'circle'))

    # Create figure with enhanced layout
    fig = go.Figure(data=[*edge_traces, node_trace],
                    layout=go.Layout(showlegend=False,
                                     hovermode='closest',
                                     margin=dict(b=0, l=0, r=0, t=0),
                                     xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                     plot_bgcolor='white'))

    return fig
