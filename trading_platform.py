#!/usr/bin/env python
import joblib
import configparser

from apscheduler.schedulers.blocking import BlockingScheduler

from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair, Gran, CandleCollector
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails

import smtplib


config = configparser.ConfigParser()
config.read('/Users/johnreichard/Documents/GitHub/Trading-Platform/config.ini')
config.sections()

gmail_config = config['GMAIL']
notifications_c = config['NOTIFICATIONS']

gmail_user = gmail_config['username']
gmail_password = gmail_config['password']
sent_from = gmail_user
to = notifications_c['email_to']
subject = 'Trading info'


