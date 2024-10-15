from datetime import datetime
import pandas as pd
from .functions import date_time_configurations_maker, dropdown_configurations_maker, radio_configuration_maker, slider_configurations_maker

df = pd.read_pickle(r'injectied_anomalies.pkl')
df = df.head(n=500)
# df.drop(columns=['Unnamed: 0'], inplace=True, axis=1)
################################################
############### Columns Configurations #########
################################################
datetime_col = 'datetime'
df[datetime_col] = pd.to_datetime(df[datetime_col])
categorical_cols = ['SrvId', 'TrxReason', 'Chanel', 'WalletNumberSender', 'WalletNumberReceiver']
bool_cols = ['IsCompleted', 'IsPosted', 'IsCliQ', 'Status']
numeric_cols = ['Fees', 'TransactionAmount', 'BalanceBefore', 'BalanceAfter', ]


id_col = 'id'
anomaly_col = 'is_anomaly'

################################################
############### Manual Configurations ##########
################################################
dashboard_name = "anomaly interactive Dashboard"


################################################
############### Columns Making #################
################################################
time_configurations = date_time_configurations_maker(df=df, datetime_col=datetime_col)
categorical_configurations = dropdown_configurations_maker(df=df, categorical_cols=categorical_cols)
bool_configurations = radio_configuration_maker(df=df, bool_cols=bool_cols)
numeric_configurations = slider_configurations_maker(df=df, num_cols=numeric_cols)

