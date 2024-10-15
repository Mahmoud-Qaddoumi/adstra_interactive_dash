import pandas as pd
import plotly.graph_objects as go

# Create DataFrame from the image data
data = {
    'SrvId': ['Srv01', 'Srv01', 'Srv01', 'Srv01', 'Srv02', 'Srv02', 'Srv02', 'Srv02',
              'Srv03', 'Srv03', 'Srv03', 'Srv03', 'Srv04', 'Srv04', 'Srv04'],
    'TrxReason': ['Payment', 'Refund', 'Transfer', 'Withdrawal', 'Payment', 'Refund', 'Transfer', 'Withdrawal',
                  'Payment', 'Refund', 'Transfer', 'Withdrawal', 'Payment', 'Refund', 'Transfer'],
    'Channel': [22, 35, 38, 22, 38, 41, 22, 32, 26, 33, 28, 32, 31, 24, 38]
}

df = pd.DataFrame(data)

# Create a mapping of SrvId and TrxReason to numeric values for plotting
srv_id_map = {srv: i for i, srv in enumerate(df['SrvId'].unique())}
trx_reason_map = {reason: i for i, reason in enumerate(df['TrxReason'].unique())}

# Create the scatter plot
fig = go.Figure()

for _, row in df.iterrows():
    fig.add_trace(go.Scatter(
        x=[srv_id_map[row['SrvId']], trx_reason_map[row['TrxReason']]],
        y=[row['SrvId'], row['TrxReason']],
        mode='lines',
        line=dict(width=row['Channel'] / 5, color='rgba(0,0,255,0.5)'),
        showlegend=False
    ))

# Customize the layout
fig.update_layout(
    title='SrvId to TrxReason Connections',
    xaxis=dict(
        tickmode='array',
        tickvals=list(srv_id_map.values()) + list(trx_reason_map.values()),
        ticktext=list(srv_id_map.keys()) + list(trx_reason_map.keys()),
        title='SrvId and TrxReason'
    ),
    yaxis=dict(title='SrvId and TrxReason'),
    height=600,
    width=800
)

# Show the plot
fig.show()