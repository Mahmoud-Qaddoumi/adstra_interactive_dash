import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple, Dict, Optional
from netgraph import Graph

# ToDo: Network Graph 1- Make the Figure Directional Diagram.
# ToDo: Network Graph 2- allow the user to change the places of the nodes using dash_cytoscape.
# ToDo: Network Graph 3- lines between nodes (size need to be increased).
# ToDo: Network Graph 4- lines between nodes (less intersection).
# ToDo: Network Graph 5- add counts to for colors options for nodes and edges.
# ToDo: Network Graph 6- appear Anomalies in Visualization.


def normalize_values(values, min_target, max_target):
    """Normalize values to a target range"""
    min_val, max_val = min(values), max(values)
    if min_val == max_val:
        return [min_target] * len(values)
    return [min_target + (max_target - min_target) * (x - min_val) / (max_val - min_val) for x in values]


def get_color_scale(values, start_color, end_color):
    """Convert normalized values to RGB colors"""
    start_rgb = np.array([int(start_color[i:i + 2], 16) for i in (1, 3, 5)])
    end_rgb = np.array([int(end_color[i:i + 2], 16) for i in (1, 3, 5)])

    normalized = np.array(normalize_values(values, 0, 1))
    colors = []

    for norm_val in normalized:
        rgb = start_rgb + (end_rgb - start_rgb) * norm_val
        rgb = rgb.astype(int)
        colors.append(f'rgb({rgb[0]},{rgb[1]},{rgb[2]})')

    return colors


def make_network_callbacks(df, left_col: str, right_col: str, circle_size_col: str, circle_color_col: str,
                           line_size_col: str, line_color_col: str, anomaly_col: str):
    """
    Create network graph with dynamic node and edge styling based on data columns.

    Parameters:
    df: DataFrame containing the network data
    left_col: Column name for source nodes
    right_col: Column name for target nodes
    circle_size_col: Column name for node sizes (numeric, scaled 1-10)
    circle_color_col: Column name for node colors (numeric, blue to red)
    line_size_col: Column name for edge widths (numeric, scaled 1-3)
    line_color_col: Column name for edge colors (numeric, green to brown)
    anomaly_col: Column name for anomaly indicators
    """
    # Create edge list with associated data
    df.to_pickle('testing.pkl')
    edges_with_data = []

    # Create node data mapping
    node_data = {}
    for _, row in df.iterrows():
        edges_with_data.append({'source': row[left_col],
                                'target': row[right_col],
                                'line_size': row[line_size_col],
                                'line_color': row[line_color_col],
                                'anomaly': row[anomaly_col]})
        for node_col in [left_col, right_col]:
            node = row[node_col]
            if node not in node_data:
                node_data[node] = {'size': row[circle_size_col],
                                   'color': row[circle_color_col],
                                   'anomaly': row[anomaly_col]}

    fig = create_network_graph(edges_with_data=edges_with_data, node_data=node_data)
    return [fig]


def create_network_graph(edges_with_data: List[dict], node_data: Dict[str, dict]):
    """
    Create an interactive network graph with dynamic styling.

    Parameters:
    edges_with_data: list of dicts containing edge information and styling data
    node_data: dict mapping node IDs to their attributes
    """
    import networkx as nx
    # Create network graph
    G = nx.DiGraph()

    # Add edges to graph
    G.add_edges_from([(edge['source'], edge['target']) for edge in edges_with_data])

    # Calculate layout
    # pos = nx.spring_layout(G, k=1 / np.sqrt(len(G.nodes())), iterations=50)
    # pos = nx.multipartite_layout(G, subset_key="target")
    pos  = pos=nx.spectral_layout(G)

    # Create edge traces with dynamic styling
    edge_traces = []
    for edge_data in edges_with_data:
        x0, y0 = pos[edge_data['source']]
        x1, y1 = pos[edge_data['target']]
        # Calculate curve control points
        dx = x1 - x0
        dy = y1 - y0
        dist = np.sqrt(dx * dx + dy * dy)

        # Adjust curve based on distance
        curve_strength = min(0.2, 2.0 / dist)

        # Calculate perpendicular vector for control point
        nx = -dy * curve_strength
        ny = dx * curve_strength

        # Create curved path
        curve_x = [x0,  x0 + dx / 2 + nx, x1]
        curve_y = [y0,  y0 + dy / 2 + ny, y1]

        # Get edge styling
        line_width = normalize_values([edge_data['line_size']], 1, 5)[0]
        line_color = get_color_scale([edge_data['line_color']], '#008000', '#8B4513')[0]  # Green to Brown

        edge_trace = go.Scatter(x=curve_x, y=curve_y, mode='lines', line=dict(width=line_width, color=line_color, shape='spline'),
                                hoverinfo='none')
        edge_traces.append(edge_trace)
        # Add arrow
        arrow_x = curve_x[-2:]
        arrow_y = curve_y[-2:]
        dx = arrow_x[1] - arrow_x[0]
        dy = arrow_y[1] - arrow_y[0]
        arrow_length = np.sqrt(dx * dx + dy * dy)

        if arrow_length > 0:
            arrow_head_x = arrow_x[1] - dx * 0.1
            arrow_head_y = arrow_y[1] - dy * 0.1
            arrow_trace = go.Scatter(x=[arrow_head_x, arrow_x[1], arrow_head_x],
                                     y=[arrow_head_y + 0.05, arrow_y[1], arrow_head_y - 0.05],
                                     mode='lines',
                                     line=dict(width=line_width, color=line_color),
                                     hoverinfo='none')
            edge_traces.append(arrow_trace)

    # Process node sizes and colors
    node_sizes = [node_data[node]['size'] for node in G.nodes()]
    node_colors = [node_data[node]['color'] for node in G.nodes()]

    # Normalize and convert to visual attributes
    normalized_node_sizes = normalize_values(node_sizes, 10, 50)  # Scale to reasonable marker sizes
    node_color_list = get_color_scale(node_colors, '#0000FF', '#FF0000')  # Blue to Red

    # Create node trace
    node_x = []
    node_y = []
    node_text = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f'Node: {node}<br>'
                         f'Size Value: {node_data[node]["size"]:.2f}<br>'
                         f'Color Value: {node_data[node]["color"]:.2f}<br>'
                         f'Anomaly: {node_data[node]["anomaly"]}')

    node_trace = go.Scatter(x=node_x, y=node_y,
                            mode='markers',
                            hoverinfo='text',
                            text=node_text,
                            marker=dict(showscale=False,
                                        color=node_color_list,
                                        size=normalized_node_sizes,
                                        line=dict(width=1, color='#888')))

    # Create figure
    fig = go.Figure(data=[*edge_traces, node_trace],
                    layout=go.Layout(showlegend=False,
                                     hovermode='closest',
                                     margin=dict(b=0, l=0, r=0, t=0),
                                     xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                     plot_bgcolor='white'))
    return fig
