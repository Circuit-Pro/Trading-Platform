#!/usr/bin/env python
from eodhd import APIClient
from os import getcwd
import configparser
import pandas as pd
from IPython.display import display


# Initialize the Parser.
config = configparser.ConfigParser()

# Read the file.
config.read(getcwd().replace('/api', '') + '/Trading-Platform/config.ini')
api_config = config['API']

def get_update(asset, search_input):

    api = APIClient(api_config['api_key'])

    resp = api.get_exchanges()
    print(resp)
    # print(resp.dtypes)
    # print(resp.describe())

    resp = api.get_exchange_symbols("US")
    print(resp)
    # print(resp.dtypes)
    # print(resp.describe())

    resp = api.get_historical_data("BTC-USD.CC", "1h")
    # resp = api.get_historical_data("BTC-USD.CC", "1m", "2021-11-27 23:56:00")
    # resp = api.get_historical_data("BTC-USD.CC", "1m", "2021-11-27 23:56:00", "2021-11-27 23:59:00")
    print(resp)
    # print(resp.dtypes)
    # print(resp.describe())

    resp = api.get_historical_data("BTC-USD.CC", "5m")
    # resp = api.get_historical_data("BTC-USD.CC", "5m", "2021-11-27 23:55:00")
    # resp = api.get_historical_data("BTC-USD.CC", "5m", "2021-11-27 23:55:00", "2021-11-28 02:00:00")
    print(resp)
    # print(resp.dtypes)
    # print(resp.describe())

    resp = api.get_historical_data("BTC-USD.CC", "1h")
    # resp = api.get_historical_data("BTC-USD.CC", "1h", "2021-11-27 23:00:00")
    # resp = api.get_historical_data("BTC-USD.CC", "1h", "2021-11-27 23:00:00", "2021-11-28 23:59:00")
    print(resp)
    # print(resp.dtypes)
    # print(resp.describe())

    resp = api.get_historical_data("BTC-USD.CC", "1d")
    # resp = api.get_historical_data("BTC-USD.CC", "1d", "2021-11-24")
    # resp = api.get_historical_data("BTC-USD.CC", "1d", "2021-11-24", "2021-11-27")
    print(resp)
    # print(resp.dtypes)
    # print(resp.describe())
    return data
    
def main():
    assets = pd.DataFrame(pd.Series(['stock', 'etf', 'fund', 'bonds', 'index', 'commodity', 'crypto'])).rename(columns = {0:'asset'})
    asset = input('Type of asset [stock, etf, fund, bonds, index, commodity, crypto]: ')

    if len(assets[assets.asset == asset]) == 0:
        print('Input Error: Asset not found', color = 'red')
    else:
        search_input = input(f'Search {asset}: ')
        print(f'\nSearch Results for {search_input}', '\n')
        search_results = get_update(asset, search_input)
        display(search_results)
if __name__ == "__main__":
    main()