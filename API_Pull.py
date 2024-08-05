from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from time import time
from time import sleep

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# Original Sandbox Environment: 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
    'start': '1',
    'limit': '15',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    # print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)


type(data)

# This allows you to see all the columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# This normalizes the data and makes it all pretty in a dataframe
df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')


def api_runner():
    global df, data
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    # Original Sandbox Environment: 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    parameters = {
        'start': '1',
        'limit': '15',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        # print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    # Use this if you just want to keep it in a dataframe
    df2 = pd.json_normalize(data['data'])
    df2['Timestamp'] = pd.to_datetime('now')
    df = df.append(df2)

    # Use this if you want to create a csv and append data to it
    # df = pd.json_normalize(data['data'])
    # df['timestamp'] = pd.to_datetime('now')


for i in range(333):
    api_runner()
    print('API Runner completed')
    sleep(60)    # Sleep for 1 minute
exit()

df72 = pd.read_csv(r'C:\Users\alexf\OneDrive\Documents\Python Scripts\API.csv')

pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Coin trends over time
df3 = df.groupby('name', sort=False)[
    ['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d',
     'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']].mean()

df4 = df3.stack()

type(df4)
df5 = df4.to_frame(name='values')
df5.count()

# Set an index
# Create a range and pass that as the dataframe
index = pd.Index(range(90))

# Set the above DataFrame index object as the index
# using set_index() function
df6 = df5.set_index(index)

# If it only has the index and values try doing reset_index like "df5.reset_index()"
# Change the column name
df7 = df6.rename(columns={'level_1': 'percent_change'})
df7['percent_change'] = df7['percent_change'].replace(
    ['quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d',
     'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d'], ['24h', '7d', '30d', '60d', '90d'])

sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')

# Create a dataframe with the columns we want
df10 = df[['name', 'quote.USD.price', 'timestamp']]
df10 = df10.query("name == 'Bitcoin'")

sns.set_theme(style="darkgrid")
sns.lineplot(x='timestamp', y='quote.USD.price', data=df10)
