#!/usr/bin/env python
import configparser
from os import *
import os
import sendgrid
from sendgrid.helpers.mail import *
import numpy as np
import pandas_ta as ta
import pandas as pd
import joblib
import datetime as dt

from apscheduler.schedulers.blocking import BlockingScheduler
import json
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair, Gran, CandleCollector, CandleClient
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails


# Load Config
config = configparser.ConfigParser()
config.read(getcwd() + '/Trading-Platform/config.ini') # Read the file.
config.sections()
gmail_config = config['GMAIL']
notifications_c = config['NOTIFICATIONS']
api_config = config['API']

# Email Config
to = notifications_c['email_to']
subject = 'Trading info'

# Load the model that we trained
loaded_model = joblib.load(getcwd() + '/Trading-Platform/Models/model.onyx')

stocks = ['MSFT']

ModelPrediction = 0
def XGB_job():
    access_token=api_config['access_token']
    client = CandleClient(access_token, real=False)
    #collector = CandleCollector(access_token, Pair.USD_JPY, Gran.D)
    collector = client.get_collector(Pair.USD_JPY, Gran.D)
    candles = collector.grab(2*161)

    dfstream = pd.DataFrame(columns=['open','close','high','low'])
    i=0
    for candle in candles:
        dfstream.loc[i, ['open']] = float(str(candle.bid.o))
        dfstream.loc[i, ['close']] = float(str(candle.bid.c))
        dfstream.loc[i, ['high']] = float(str(candle.bid.h))
        dfstream.loc[i, ['low']] = float(str(candle.bid.l))
        i=i+1

    dfstream['open'] = dfstream['open'].astype(float)
    dfstream['close'] = dfstream['close'].astype(float)
    dfstream['high'] = dfstream['high'].astype(float)
    dfstream['low'] = dfstream['low'].astype(float)

   
    import numpy as np
    import pandas_ta as ta
    dfstream['ATR'] = dfstream.ta.atr(length=20)
    dfstream['RSI'] = dfstream.ta.rsi()

    #________________________________________________________________________________________________
    X_stream = dfstream.iloc[[319,320]].copy()# !!! Index takes last CLOSED candle and the one before
    X_stream.reset_index(drop=True, inplace=True)
    signal = 0
    length = len(X_stream)

    highdiff = [0] * length
    lowdiff = [0] * length
    bodydiff = [0] * length
    ratio1 = [0] * length
    ratio2 = [0] * length
   
    #print(X_stream.high[0])

    for row in range(0,length):
        highdiff[row] = X_stream.high[row]-max(X_stream.open[row],X_stream.close[row])
        bodydiff[row] = abs(X_stream.open[row]-X_stream.close[row])
        if bodydiff[row]<0.002:
            bodydiff[row]=0.002
        lowdiff[row] = min(X_stream.open[row],X_stream.close[row])-X_stream.low[row]
        ratio1[row] = highdiff[row]/bodydiff[row]
        ratio2[row] = lowdiff[row]/bodydiff[row]

    row=1
    if (ratio1[row]>2.5 and lowdiff[row]<0.3*highdiff[row] and bodydiff[row]>0.03 and X_stream.RSI[row]>50 and X_stream.RSI[row]<70 ):
        signal = 1
    elif (ratio2[row-1]>2.5 and highdiff[row-1]<0.23*lowdiff[row-1] and bodydiff[row-1]>0.03 and bodydiff[row]>0.04 and X_stream.Close[row]>X_stream.open[row] and X_stream.close[row]>X_stream.high[row-1] and X_stream.RSI[row]<55 and X_stream.RSI[row]>30):
        signal = 2
    else:
        signal = 0
    
    
    #------------------------------------
    # send email with 
    sg = sendgrid.SendGridAPIClient(api_key='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')
    from_email = Email("sheila@mrhousepb.com")
    msg = str(signal)+" TEST  "
    mail = Mail(from_email, to, subject, msg)
    sg.client.mail.send.post(request_body=mail.get())
    #print(response.status_code)
    #print(response.body)
    #print(response.headers)
    #________________________________________________________________________________________________
    
    # EXECUTING ORDERS
    
    accountID = api_config['account_id'] #your account ID here
    client = API(access_token)
    
    candles = collector.grab(1)
    for candle in candles:
        print(candle.bid.o)
        print(candle.bid.c)
        print(candle.bid.h)
        print(candle.bid.l)
    
    pipdiff = X_stream.ATR[row]*1. #highdiff*1.3 #for SL 400*1e-3
    if pipdiff<1.1:
        pipdiff=1.1
            
    SLTPRatio = 2. #pipdiff*Ratio gives TP
    
    TPBuy = float(str(candle.bid.o))+pipdiff*SLTPRatio
    SLBuy = float(str(candle.bid.o))-pipdiff
    TPSell = float(str(candle.bid.o))-pipdiff*SLTPRatio
    SLSell = float(str(candle.bid.o))+pipdiff
    
    print(TPBuy, "  ", SLBuy, "  ", TPSell, "  ", SLSell)
    
    #Sell
    if signal == 1:
        mo = MarketOrderRequest(instrument="USD_JPY", units=-1000, takeProfitOnFill=TakeProfitDetails(price=TPSell).data, stopLossOnFill=StopLossDetails(price=SLSell).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
    #Buy
    elif signal == 2:
        mo = MarketOrderRequest(instrument="USD_JPY", units=1000, takeProfitOnFill=TakeProfitDetails(price=TPBuy).data, stopLossOnFill=StopLossDetails(price=SLBuy).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)

XGB_job()
## Interval time job scheduler ##
scheduler = BlockingScheduler(job_defaults={'misfire_grace_time': 15*60})
scheduler.add_job(XGB_job, 'cron', day_of_week='mon-fri', minute=1, jitter=120, timezone='America/New_York')
#scheduler.add_job(XGB_job, 'interval', hours=4)
scheduler.start()

