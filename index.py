from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import streamlit as sl
import pandas as pd
import matplotlib.pyplot as plt

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

symbols = []

print(symbols)

sl.sidebar.header('Input Options')

coin_number = sl.sidebar.slider("Number of the top cryptocurrencies you're searching for:", 1, 50, 50)

data = data[0:coin_number]

for point in data:    
    symbol = point["symbol"]
    symbols.append(symbol)

symbols = symbols[0:coin_number]

sl.sidebar.multiselect('Cryptocurrency', symbols, symbols)

sl.sidebar.selectbox('Time frame for percent change', ['7d', '24h', '1h'])

name_array = [] 
symbol_array = []
price_array = []
volume_24h_array = []
volume_change_24h_array = []
percent_change_1h_array = []
percent_change_24h_array = []
percent_change_7d_array = []
market_cap_array = []

def add_data_to_table():
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
        price_array.append("{:,.2f}".format(price))
        volume_24h_array.append("{:,.2f}".format(volume_24h))
        volume_change_24h_array.append("{:,.2f}".format(volume_change_24h))
        percent_change_1h_array.append("{:,.2f}".format(percent_change_1h))
        percent_change_24h_array.append("{:,.2f}".format(percent_change_24h))
        percent_change_7d_array.append("{:,.2f}".format(percent_change_7d))
        market_cap_array.append("{:,.2f}".format(market_cap))

add_data_to_table()

sl.title("Crypto Data Science App")

sl.image("crypto-app-logo.jpeg")

# creating table
# create array for each column
sl.write("Top 25 Cryptocurrencies")

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
sl.subheader('Positive percent change in crypto price')
fig = plt.figure()
ax = fig.add_axes([0, 0, 2, 2])
crypto_symbols = symbol_array
percent_change = percent_change_7d_array
ax.bar(crypto_symbols, percent_change)
plt.xticks(rotation=70)
fig.canvas.draw()
sl.pyplot(plt)

sl.subheader('Negative percent change in crypto price')
fig = plt.figure()
ax = fig.add_axes([0, 0, 2, 2])
crypto_symbols = symbol_array
percent_change = percent_change_7d_array
ax.bar(crypto_symbols, percent_change)
plt.xticks(rotation=70)
plt.xticks(rotation=70)

fig.canvas.draw()
sl.pyplot(plt)