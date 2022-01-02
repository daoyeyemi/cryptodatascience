from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import streamlit as sl
import pandas as pd

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

parameters = {
    'start' : '1',
    'limit' : '5000',
    'convert' : 'USD'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '66d451b5-daf2-4106-8381-1c9d30351983'
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
sl.title("Crypto Data Science App")
sl.image("crypto-app-logo.jpeg")

# creating table
# create array for each column
name = [1, 2, 3, 4, 5, 6] 
symbol = [1, 2, 3, 4, 5, 6]
price = [1, 2, 3, 4, 5, 6]
volume_24h = [1, 2, 3, 4, 5, 6]
volume_change_24h = [1, 2, 3, 4, 5, 6]
percent_change_1h = [1, 2, 3, 4, 5, 6]
percent_change_24h = [1, 2, 3, 4, 5, 6]
percent_change_7d = [1, 2, 3, 4, 5, 6]
market_cap = [1, 2, 3, 4, 5, 6]

def show_table():
    crypto_data_table = pd.DataFrame(columns=['name', 'symbol', 'price', 'volume_24h', 'volume_change_24h', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'market_cap'])
    crypto_data_table['name'] = name
    crypto_data_table['symbol'] = symbol
    crypto_data_table['price'] = price
    crypto_data_table['volume_24h'] = volume_24h
    crypto_data_table['volume_change_24h'] = volume_change_24h
    crypto_data_table['percent_change_1h'] = percent_change_1h
    crypto_data_table['percent_change_24h'] = percent_change_24h
    crypto_data_table['percent_change_7d'] = percent_change_7d
    crypto_data_table['market_cap'] = market_cap
    sl.table(crypto_data_table)

show_table()

