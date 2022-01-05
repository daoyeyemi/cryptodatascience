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
#   print(data, type(data))

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

data = data["data"]

name_array = [] 
symbol_array = []
price_array = []
volume_24h_array = []
volume_change_24h_array = []
percent_change_1h_array = []
percent_change_24h_array = []
percent_change_7d_array = []
market_cap_array = []

for point in data:
    name = point["name"]
    symbol = point["symbol"]
    price = point["quote"]["USD"]["price"]
    print(price)
    volume_24h = point["quote"]["USD"]["volume_24h"]
    volume_change_24h = point["quote"]["USD"]["volume_change_24h"]
    percent_change_1h = point["quote"]["USD"]["percent_change_1h"]
    percent_change_24h = point["quote"]["USD"]["percent_change_24h"]
    percent_change_7d = point["quote"]["USD"]["percent_change_7d"]
    market_cap = point["quote"]["USD"]["market_cap"]

    name_array.append(name)
    symbol_array.append(symbol)
    price_array.append("{:.2f}".format(price))
    volume_24h_array.append(volume_24h)
    volume_change_24h_array.append(volume_change_24h)
    percent_change_1h_array.append(percent_change_1h)
    percent_change_24h_array.append(percent_change_24h)
    percent_change_7d_array.append(percent_change_7d)
    market_cap_array.append(market_cap)


sl.title("Crypto Data Science App")

sl.image("crypto-app-logo.jpeg")

# creating table
# create array for each column


def show_table():
    crypto_data_table = pd.DataFrame(columns=['name', 'symbol', 'price', 'volume_24h', 'volume_change_24h', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'market_cap'])
    crypto_data_table['name'] = name_array
    crypto_data_table['symbol'] = symbol_array
    crypto_data_table['price'] = price_array
    crypto_data_table['volume_24h'] = volume_24h_array
    crypto_data_table['volume_change_24h'] = volume_change_24h_array
    crypto_data_table['percent_change_1h'] = percent_change_1h_array
    crypto_data_table['percent_change_24h'] = percent_change_24h_array
    crypto_data_table['percent_change_7d'] = percent_change_7d_array
    crypto_data_table['market_cap'] = market_cap_array
    sl.table(crypto_data_table)

show_table()