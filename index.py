from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import streamlit as sl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

parameters = {
    'start' : '1',
    'limit' : '5000',
    'convert' : 'USD'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '64cd695d-26ab-4937-b788-14b86a0db2f8'
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  crypto_data = json.loads(response.text)
#   print(crypto_data, type(crypto_data))

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

yooo = crypto_data['data']

symbols = []

sl.sidebar.header('Input Options')

coin_number = sl.sidebar.slider("Number of the top cryptocurrencies you're searching for:", 1, 50, 50)

yooo = yooo[0:coin_number]

for point in yooo:    
    symbol = point["symbol"]
    symbols.append(symbol)

symbols = symbols[0:coin_number]

sl.sidebar.multiselect('Cryptocurrency', symbols, symbols)

time_frame_percent = sl.sidebar.selectbox('Time frame for percent change', ['7d', '24h', '1h'])

name_array = [] 
symbol_array = []
price_array = []
volume_24h_array = []
volume_change_24h_array = []
percent_change_1h_array = []
percent_change_24h_array = []
percent_change_7d_array = []
market_cap_array = []

# def add_data_to_table():
for point in yooo:
    name = point["name"]
    symbol = point["symbol"]
    price = point["quote"]["USD"]["price"]
    volume_24h = point["quote"]["USD"]["volume_24h"]
    volume_change_24h = point["quote"]["USD"]["volume_change_24h"]
    percent_change_1h = point["quote"]["USD"]["percent_change_1h"]
    print(percent_change_1h)
    percent_change_24h = point["quote"]["USD"]["percent_change_24h"]
    percent_change_7d = point["quote"]["USD"]["percent_change_7d"]
    market_cap = point["quote"]["USD"]["market_cap"]

    name_array.append(name)
    symbol_array.append(symbol)
    price_array.append("{:,.2f}".format(price))
    volume_24h_array.append("{:,.2f}".format(volume_24h))
    volume_change_24h_array.append("{:,.2f}".format(volume_change_24h))
    # percent_change_1h_array.append("{:,.2f}".format(percent_change_1h))
    # percent_change_24h_array.append("{:,.2f}".format(percent_change_24h))
    # percent_change_7d_array.append("{:,.2f}".format(percent_change_7d))
    percent_change_1h_array.append(percent_change_1h)
    percent_change_24h_array.append(percent_change_24h)
    percent_change_7d_array.append(percent_change_7d)
    market_cap_array.append("{:,.2f}".format(market_cap))
        
    # percent_change_1h_array = list(map(int, percent_change_1h_array))
    # percent_change_24h_array = list(map(int, percent_change_24h_array))
    # percent_change_7d_array = list(map(int, percent_change_7d_array))

# add_data_to_table()

sl.title("Crypto Data Science App")

sl.image("crypto-app-logo.jpeg")

# creating table
# create array for each column
sl.write("Top 25 Cryptocurrencies")

# def show_tables():
# percent_change_1h_array = list(map(float, percent_change_1h_array))
# percent_change_1h_array = list(map(int, percent_change_1h_array))
print(percent_change_1h_array)
# percent_change_24h_array = list(map(float, percent_change_24h_array))
# percent_change_7d_array = list(map(float, percent_change_7d_array))

crypto_data_table = pd.DataFrame(columns=['name', 'symbol', 'price', 'volume_24h', 'volume_change_24h', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'market_cap'])
crypto_data_table['name'] = name_array
crypto_data_table['symbol'] = symbol_array
crypto_data_table['price'] = price_array
crypto_data_table['volume_24h'] = volume_24h_array
crypto_data_table['volume_change_24h'] = volume_change_24h_array
crypto_data_table['percent_change_1h'] = percent_change_1h_array
print(percent_change_1h_array)
crypto_data_table['percent_change_24h'] = percent_change_24h_array
crypto_data_table['percent_change_7d'] = percent_change_7d_array
crypto_data_table['market_cap'] = market_cap_array
sl.table(crypto_data_table)

# show_tables() 
sl.subheader('Percent changes in crypto price')
positive_percent_change_dataframe = pd.DataFrame(columns=['name', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d'])
fig = plt.figure()
ax = fig.add_axes([0, 0, 2, 2])
crypto_symbols = symbol_array
if time_frame_percent == '7d':
    percent_change = percent_change_7d_array
elif time_frame_percent == '24h':
    percent_change = percent_change_24h_array
else:
    percent_change = percent_change_1h_array

# percent_change = percent_change_7d_array
# positive_percent_change_dataframe['percent_change_1h'] = percent_change_1h_array >= 0 
# positive_percent_change_dataframe['percent_change_24h'] = percent_change_24h_array >= 0
# positive_percent_change_dataframe['percent_change_7d'] = percent_change_7d_array >= 0
ax.bar(crypto_symbols, percent_change, color='blue')
plt.xticks(rotation=70)
fig.canvas.draw()
sl.pyplot(plt)

# sl.subheader('Negative percent change in crypto price')
# negative_percent_change_dataframe = pd.DataFrame(columns=['name', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d'])
# fig = plt.figure()
# ax = fig.add_axes([0, 0, 2, 2])
# crypto_symbols = symbol_array
# percent_change = percent_change_7d_array
# # negative_percent_change_dataframe['percent_change_1h'] = percent_change_1h_array < 0 
# # negative_percent_change_dataframe['percent_change_24h'] = percent_change_24h_array < 0 
# # negative_percent_change_dataframe['percent_change_7d'] = percent_change_7d_array < 0 
# ax.bar(crypto_symbols, percent_change, color='red')
# plt.xticks(rotation=70)
# fig.canvas.draw()
# sl.pyplot(plt)