#!/usr/bin/env python
import configparser
from os import getcwd
import numpy as np
import pandas_ta as ta
import pandas as pd
import joblib
import datetime as dt

from apscheduler.schedulers.blocking import BlockingScheduler

from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
#from oanda_candles import Pair, Gran, CandleCollector
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from scipy.stats import linregress

import smtplib

# API libary
import yfinance
#import td_api
#import EODHD_API


# Load Config
config = configparser.ConfigParser()
config.read(getcwd() + '/Trading-Platform/config.ini') # Read the file.
config.sections()
gmail_config = config['GMAIL']
notifications_c = config['NOTIFICATIONS']

# Email Config
gmail_user = gmail_config['username']
gmail_password = gmail_config['password']
sent_from = gmail_user
to = notifications_c['email_to']
subject = 'Trading info'

# Load the model that we trained
loaded_model = joblib.load(getcwd() + '/Trading-Platform/Models/model.onyx')

stocks = ['MSFT']

ModelPrediction = 0
def XGB_job(stock_data):
    # Assign the 'stock_data' DataFrame to the 'candles' variable
    candles = stock_data

    # Initialize an empty DataFrame with columns 'Open', 'Close', 'High', and 'Low'
    dfstream = pd.DataFrame(columns=['Open','Close','High','Low'])
    i=0

    # Iterate over the rows in the 'candles' DataFrame
    for index, row in candles.iterrows():
        # Assign the values in the 'Open', 'Close', 'High', and 'Low' columns to the corresponding columns in the 'dfstream' DataFrame
        dfstream.loc[i, ['Open']] = row['Open']
        dfstream.loc[i, ['Close']] = row['Close']
        dfstream.loc[i, ['High']] = row['High']
        dfstream.loc[i, ['Low']] = row['Low']
        i=i+1

    # Convert the 'Open', 'Close', 'High', and 'Low' columns to float data type
    dfstream['Open'] = dfstream['Open'].astype(float)
    dfstream['Close'] = dfstream['Close'].astype(float)
    dfstream['High'] = dfstream['High'].astype(float)
    dfstream['Low'] = dfstream['Low'].astype(float)

    #dfstream['Average'] = (dfstream['High']+dfstream['Low'])/2
    #dfstream['MA40'] = dfstream['Open'].rolling(window=40).mean()
    #dfstream['MA80'] = dfstream['Open'].rolling(window=80).mean()
    #dfstream['MA160'] = dfstream['Open'].rolling(window=160).mean()
    

    #attributes=['ATR', 'RSI', 'Average', 
    #'MA40', 'MA80', 'MA160', 'slopeMA40', 
    #'slopeMA80', 'slopeMA160', 'AverageSlope', 'RSISlope']
    dfstream['ATR'] = ta.atr(dfstream['High'], dfstream['Low'], dfstream['Close'], length=20)
    dfstream['RSI'] = ta.rsi(dfstream['Close'])
    dfstream['Average'] = ta.midprice(dfstream['High'], dfstream['Low'], length=1) #midprice
    dfstream['MA40'] = ta.sma(dfstream['Close'], length=40)
    dfstream['MA80'] = ta.sma(dfstream['Close'], length=80)
    dfstream['MA160'] = ta.sma(dfstream['Close'], length=160)


    def get_slope(array):
        y = np.array(array)
        x = np.arange(len(y))
        slope, intercept, r_value, p_value, std_err = linregress(x,y)
        return slope

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    backrollingN = 6
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    dfstream['slopeMA40'] = dfstream['MA40'].rolling(window=backrollingN).apply(get_slope, raw=True)
    dfstream['slopeMA80'] = dfstream['MA80'].rolling(window=backrollingN).apply(get_slope, raw=True)
    dfstream['slopeMA160'] = dfstream['MA160'].rolling(window=backrollingN).apply(get_slope, raw=True)
    dfstream['AverageSlope'] = dfstream['Average'].rolling(window=backrollingN).apply(get_slope, raw=True)
    dfstream['RSISlope'] = dfstream['RSI'].rolling(window=backrollingN).apply(get_slope, raw=True)


    X_stream = dfstream.iloc[-1]# !!! Index takes last CLOSED candle
    attributes=['ATR', 'RSI', 'Average', 'MA40', 'MA80', 'MA160', 
    'slopeMA40', 'slopeMA80', 'slopeMA160', 'AverageSlope', 'RSISlope']
    X_model = X_stream[attributes]
    
    # Apply the model for predictions
    ModelPrediction = loaded_model.predict(X_model)
  
    msg = str(ModelPrediction) # 0 no clear trend, 1 downtrend, 2 uptrend

    # send email with Gmail if there is a clear trend or downtrend
    if msg > 0:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, msg)
        server.close()
    
    # EXECUTING ORDERS

    candles = stock_data
    
    pipdiff = 500*1e-5 #for TP
    SLTPRatio = 2 #pipdiff/Ratio gives SL
    
    TPBuy = float(str(candle.bid.o))+pipdiff
    SLBuy = float(str(candle.bid.o))-(pipdiff/SLTPRatio)
    TPSell = float(str(candle.bid.o))-pipdiff
    SLSell = float(str(candle.bid.o))+(pipdiff/SLTPRatio)
    
    #Sell
    if ModelPrediction == 1:
        print("Model Prediction:", ModelPrediction)
        #mo = MarketOrderRequest(instrument="USD_CHF", units=-1000, takeProfitOnFill=TakeProfitDetails(price=TPSell).data, stopLossOnFill=StopLossDetails(price=SLSell).data)
        #r = orders.OrderCreate(accountID, data=mo.data)
        #rv = client.request(r)
        #print(rv)
    #Buy
    elif ModelPrediction == 2:
        print("Model Prediction:", ModelPrediction)
        #mo = MarketOrderRequest(instrument="USD_CHF", units=1000, takeProfitOnFill=TakeProfitDetails(price=TPBuy).data, stopLossOnFill=StopLossDetails(price=SLBuy).data)
        #r = orders.OrderCreate(accountID, data=mo.data)
        #rv = client.request(r)
        #print(rv)


## Interval time job scheduler ##
#scheduler = BlockingScheduler(job_defaults={'misfire_grace_time': 15*60})
#scheduler.add_job(XGB_job, 'cron', day_of_week='mon-fri', hour='*/4', minute=5, jitter=120, timezone='America/New_York')
#scheduler.add_job(some_job, 'interval', hours=4)
#scheduler.start()
XGB_job(yfinance.download(stocks, start='2022-01-01', end='2023-01-04', group_by='ticker'))
print(yfinance.download(stocks, start='2022-01-01', end='2023-01-04', group_by='ticker'))