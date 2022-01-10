from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import streamlit as sl
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv 
import os

## To List
# - hide api key
# - clean comments
# - color code graph
# - 'objectify' code 
# change layout of app

load_dotenv()

api_key = os.getenv("api_key")

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

parameters = {
    'start' : '1',
    'limit' : '5000',
    'convert' : 'USD'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key
}

session = Session()
session.headers.update(headers)

# try:
response = session.get(url, params=parameters)
crypto_data = json.loads(response.text)

# except (ConnectionError, Timeout, TooManyRedirects) as e:
#   print(e)

yooo = crypto_data['data']

sl.sidebar.header('Input Options')

coin_number = sl.sidebar.slider("Number of the top cryptocurrencies you're searching for:", 1, 50, 50)

yooo = yooo[0:coin_number]

name_array = [] 
symbol_array = []
price_array = []
volume_24h_array = []
volume_change_24h_array = []
percent_change_1h_array = []
percent_change_24h_array = []
percent_change_7d_array = []
market_cap_array = []


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
    percent_change_1h_array.append(percent_change_1h)
    percent_change_24h_array.append(percent_change_24h)
    percent_change_7d_array.append(percent_change_7d)
    market_cap_array.append("{:,.2f}".format(market_cap))

sl.title("Crypto Data Science App")

sl.image("crypto-app-logo.jpeg")

sl.write("Top 25 Cryptocurrencies")

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


all_coins = crypto_data_table['symbol']

crypto_coins_selected = sl.sidebar.multiselect('Cryptocurrency', all_coins, all_coins)
# all cryptocurrencies that are included in multiselect will be included here
# filtering data based on
# if crypto_coins_selected are in the 'symbol' part of dataframe then they are now part of the 'crypto_dataframe'
crypto_coins = crypto_data_table[ (crypto_data_table['symbol'].isin(crypto_coins_selected)) ]

crypto_dataframe = crypto_coins[0:coin_number]

sl.table(crypto_dataframe)

time_frame_percent = sl.sidebar.selectbox('Time frame for percent change', ['7d', '24h', '1h'])

sl.subheader('Bar plot of percent changes in crypto price')
subheader_percent_changes = 0;
positive_percent_change_dataframe = pd.DataFrame(columns=['name', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d'])
fig = plt.figure()
ax = fig.add_axes([0, 0, 2, 2])
crypto_symbols = symbol_array
if time_frame_percent == '7d':
    percent_change = percent_change_7d_array
    subheader_percent_changes = sl.write('*percent changes within a 7 day period*')
elif time_frame_percent == '24h':
    percent_change = percent_change_24h_array
    subheader_percent_changes = sl.write('*percent changes within a 24 hour period*')
else:
    percent_change = percent_change_1h_array
    subheader_percent_changes = sl.write('*percent changes within an hour period*')

ax.bar(crypto_symbols, percent_change, color='blue')
plt.xticks(rotation=70)
plt.xlabel("Cryptocurrency")
plt.ylabel("Percentage change within specified time period")
fig.canvas.draw()
sl.pyplot(plt)