#!/usr/bin/env python
from pprint import pprint
from os import getcwd
import requests
import json
import configparser
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient

# TD, Think Or Swim
# Credentials path is required.
credentials_path = getcwd() + '/credentials.json'

# Initialize the Parser.
config = configparser.ConfigParser()

# Read the file.
config.read(getcwd() + '/Trading-Platform/config.ini')

# Get the specified credentials.
client_id = config.get('main', 'client_id')
redirect_uri = config.get('main', 'redirect_uri')

# Intialize our `Credentials` object.
td_credentials = TdCredentials(
    client_id=client_id,
    redirect_uri=redirect_uri,
    credential_file=credentials_path #'config/td_credentials.json'
)
# Initalize the `TdAmeritradeClient`
td_client = TdAmeritradeClient(
    credentials=td_credentials
)

# Initialize the Quotes service.
quote_service = td_client.quotes()
# Initialize the Movers service.
movers_service = td_client.movers()
# Initialize the Accounts service.
accounts_service = td_client.accounts()
# Initialize the Market Hours service.
market_hours_service = td_client.market_hours()
# Initialize the Instruments service.
instruments_service = td_client.instruments()
# Initialize the Price History service.
price_history_service = td_client.price_history()
# Initialize the Options Chain service.
options_chain_service = td_client.options_chain()
# Initialize the Watch List service.
watchlists_service = td_client.watchlists()
# Initialize the Orders Service.
orders_service = td_client.orders()
# Initialize the Saved Orders service.
saved_orders_service = td_client.saved_orders()
# Initialize the Streaming API service.
streaming_api_service = td_client.streaming_api_client()

# Grab a single quote.
pprint(
    quote_service.get_quote(instrument='AAPL')
)

# Grab multiple quotes.
pprint(
    quote_service.get_quotes(instruments=['AAPL', 'SQ'])
)

stock_tickers = ['AAPL', 'MSFT', 'GOOGL', 'NFLX'] # basic stock tickers for tests

# Stock Quotes
def get_stock_quotes(stock_tickers):
        # Grab real-time quotes
    quotes = TDSession.get_quotes(instruments=stock_tickers)

# Historical Price - Basic

def get_historical_price(stock_ticker):
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory'
    full_url = endpoint.format(stock_ticker)
    page = requests.get(url=full_url,params={'apikey' : td_consumer_key})
    stock_data = json.loads(page.content)
    if page.status_code == 200:
        #stock_data = page.json()['results']
        print(stock_ticker,":", stock_data)
        return stock_data
    else:
        print(page.status_code)

# Historical Price - Advanced

def get_historical_price_advanced(stock_ticker, periodType, period, frequencyType, frequency):
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'
    full_url = endpoint.format(stock_ticker,periodType,period,frequencyType,frequency)
    page = requests.get(url=full_url,params={'apikey' : td_consumer_key})
    stock_data = json.loads(page.content)
    if page.status_code == 200:
        #stock_data = page.json()['results']
        print(stock_ticker,":", stock_data)
        return stock_data
    else:
        print(page.status_code)

# Fundamentals Data
def get_fundamentals_data(stock_ticker):
    base_url = 'https://api.tdameritrade.com/v1/instruments?&symbol={stock_ticker}&projection={projection}'
    endpoint = base_url.format(stock_ticker, projection = 'fundamental')
    page = requests.get(url=endpoint, params={'apikey' : td_consumer_key})
    stock_data = json.loads(page.content)
    if page.status_code == 200:
        #stock_data = page.json()['results']
        print(stock_ticker,":", stock_data)
        return stock_data
    else:
        print(page.status_code)

# Options Data - Basic
def get_options_data(stock_ticker):
    base_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}'
    endpoint = base_url.format(stock_ticker)
    page = requests.get(url=endpoint, 
            params={'apikey' : td_consumer_key})
    stock_data = json.loads(page.content)
    if page.status_code == 200:
        #stock_data = page.json()['results']
        print(stock_ticker,":", stock_data)
        return stock_data
    else:
        print(page.status_code)

# Options Data - Advanced
def get_options_data_advanced(stock_ticker, contractType, date):
    base_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}&contractType={contractType}&fromDate={date}&toDate={date}'
    endpoint = base_url.format(stock_ticker, contractType, date) #date yyyy-mm-dd
    page = requests.get(url=endpoint, params={'apikey' : td_consumer_key})
    stock_data = json.loads(page.content)
    if page.status_code == 200:
        #stock_data = page.json()['results']
        print(stock_ticker,":", stock_data)
        return stock_data
    else:
        print(page.status_code)

# Options Data - Advanced - Strike Price
def get_options_data_advanced_strike_price(stock_ticker, contractType, date, strike_price):
    base_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}\
    &contractType={contract_type}&strike={strike}&fromDate={date}&toDate={date}'
    endpoint = base_url.format(stock_ticker, contractType , strike_price, date)
    page = requests.get(url=endpoint, params={'apikey' : td_consumer_key})
    stock_data = json.loads(page.content)
    if page.status_code == 200:
        #stock_data = page.json()['results']
        print(stock_ticker,":", stock_data)
        return stock_data
    else:
        print(page.status_code)


for ticker in stock_tickers: # itterate through all stock tickers since we can only get one at a time.
    stock_ticker = ticker.upper()