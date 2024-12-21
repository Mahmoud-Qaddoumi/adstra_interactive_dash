from datetime import datetime, timedelta
import pandas as pd
from configurations.functions import date_time_configurations_maker, dropdown_configurations_maker, \
    radio_configuration_maker, slider_configurations_maker, get_exact_query, make_query, format_date

data_db_config = ("DRIVER={ODBC Driver 17 for SQL Server};"
                  "SERVER=localhost\\SQLEXPRESS01;"
                  "DATABASE=A2A.eWallet;"
                  "Trusted_Connection=yes;")

anomalies_db_config = ("DRIVER={ODBC Driver 17 for SQL Server};"
                       "SERVER=localhost\\SQLEXPRESS01;"
                       "DATABASE=A2A.eWallet;"
                       "Trusted_Connection=yes;")

################################################
############### Columns Configurations #########
################################################
datetime_col = 'Date'
cat_cols = ['TransactionEName', 'Status']
target_col = 'WalletNumberSender'
bool_cols = []
num_cols = ['Amount', 'TotalAmount', 'Fees', 'ExtraCharge']
period_to_analyse = 120
id_col = 'RefernceNumber'
anomaly_col = 'is_anomaly'
db_table_name = 'sample_of_2'
anomaly_table = 'anomaly_result'
################################################
############### Manual Configurations ##########
################################################
dashboard_name = "anomaly Dashboard"

################################################
############### Columns Making #################
################################################
to_date = datetime.today()
from_date = datetime.now() - timedelta(days=period_to_analyse)
cat_cols.append(target_col)
sql_query = make_query(table_name=db_table_name,
                       id_column=id_col,
                       date_column=datetime_col,
                       categorical_columns=cat_cols,
                       numerical_columns=num_cols,
                       boolean_columns=bool_cols,
                       start_date=from_date.strftime('%Y-%m-%d'),
                       end_date=to_date.strftime('%Y-%m-%d'),
                       limit=0)

df = get_exact_query(query=sql_query, db_details=data_db_config)

anomaly_query = f"""
SELECT *
FROM {anomaly_table} 
WHERE CAST(datetime AS DATE) 
BETWEEN '{format_date(from_date.strftime('%Y-%m-%d'))}' 
AND '{format_date(to_date.strftime('%Y-%m-%d'))}'
"""

anomalies_df = get_exact_query(query=anomaly_query, db_details=data_db_config)
for col in cat_cols:
    df[col] = df[col].astype('str')
anomalies_df.columns = [id_col, 'anomaly_score', 'is_anomaly', 'datetime']
anomalies_df.to_pickle('anomalies.pkl')
df[datetime_col] = pd.to_datetime(df[datetime_col])
# anomalies_df = anomalies_df[anomalies_df['anomaly_score']> 5]
df.to_pickle('original.pkl')
df = pd.merge(left=df, right=anomalies_df, how='left', on=[id_col], )
# df= anomalies_df.join(df,on=id_col,how='left')
# df = df.fillna(False)
df.to_pickle('test.pkl')
time_configurations = date_time_configurations_maker(df=df, datetime_col=datetime_col)
categorical_configurations = dropdown_configurations_maker(df=df, categorical_cols=cat_cols)
bool_configurations = radio_configuration_maker(df=df, bool_cols=bool_cols)
numeric_configurations = slider_configurations_maker(df=df, num_cols=num_cols)
