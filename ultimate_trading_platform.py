import tkinter as tk
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import yfinance as yf
import tensorflow as tf
import time
import tradestation_api as ts
from textblob import TextBlob

# Data Gathering
def gather_data(symbols, start_date, end_date):
  data = {}
  for symbol in symbols:
    data[symbol] = yf.download(symbol, start_date, end_date)
    data[symbol]['News'] = ts.get_news(symbol) # get news from TradeStation
  return data

# Data Preprocessing
def preprocess_data(data):
  processed_data = {}
  for symbol, df in data.items():
    df = df.dropna()
    df['Returns'] = df['Adj Close'].pct_change()
    df = df[['Adj Close', 'Returns']]
    df['Sentiment'] = df['News'].apply(lambda x: TextBlob(x).sentiment.polarity) # calculate sentiment
    processed_data[symbol] = df
  return processed_data

# Feature Engineering
def extract_features(processed_data, window_size):
  features = {}
  for symbol, df in processed_data.items():
    df['SMA'] = df['Adj Close'].rolling(window=window_size).mean()
    df['EWMA'] = df['Adj Close'].ewm(span=window_size).mean()
    df['ROC'] = df['Adj Close'].diff(periods=1) / df['Adj Close'].shift(periods=1)
    df['Sentiment'] = df['Sentiment'].shift(-1) # shift sentiment one day forward
    df['Returns'] = df['Returns'].shift(-1)
    df = df[['SMA', 'EWMA', 'ROC', 'Sentiment', 'Returns']]
    df = df.dropna()
    features[symbol] = df
  return features

# Train Model
def train_model(features, labels):
  X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
  scaler = MinMaxScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)
  model = LinearRegression()
  model.fit


# Continuous Learning
def continuous_learning(model, scaler, data, window_size):
  while True:
    processed_data = preprocess_data(data)
    features = extract_features(processed_data, window_size)
    labels = []
    for symbol, df in features.items():
      labels.append(df['Returns'])
    labels = pd.concat(labels)
    model, scaler = train_model(features, labels)
    time.sleep(3600) # retrain model every
    
class App(tk.Tk):
  def __init__(self):
    tk.Tk.__init__(self)
    self.title("Trading AI")

    # Create top menu
    self.menu = tk.Menu(self)
    self.config(menu=self.menu)
    self.menu_file = tk.Menu(self.menu)
    self.menu.add_cascade(label="File", menu=self.menu_file)
    self.menu_file.add_command(label="Add Ticker", command=self.add_ticker)
    self.menu_file.add_command(label="Remove Ticker", command=self.remove_ticker)

    # Create tabs
    self.tabs = tk.Notebook(self)
    self.tab_overview = tk.Frame(self.tabs)
    self.tab_tickers = tk.Frame(self.tabs)
    self.tab_best_stocks = tk.Frame(self.tabs)
    self.tabs.add(self.tab_overview, text="Overview")
    self.tabs.add(self.tab_tickers, text="Tickers")
    self.tabs.add(self.tab_best_stocks, text="Best Stocks")
    self.tabs.pack(expand=1, fill='both')

    # Overview tab
    self.label_overview = tk.Label(self.tab_overview, text="Welcome to the Trading AI!")
    self.label_overview.pack()
    self.button_overview = tk.Button(self.tab_overview, text="Start Trading", command=self.start_trading)
    self.button_overview.pack()

    # Tickers tab
    self.label_tickers = tk.Label(self.tab_tickers, text="Tickers:")
    self.label_tickers.pack()
    self.listbox_tickers = tk.Listbox(self.tab_tickers)
    self.listbox_tickers.pack()
    self.button_tickers = tk.Button(self.tab_tickers, text="Update Tickers", command=self.update_tickers)
    self.button_tickers.pack()

    # Best Stocks tab
    self.label_best_stocks = tk.Label(self.tab_best_stocks, text="Best Stocks:")
    self.label_best_stocks.pack()
    self.listbox_best_stocks = tk.Listbox(self.tab_best_stocks)
    self.listbox_best_stocks.pack()
    self.button_best_stocks = tk.Button(self.tab_best_stocks, text="Update Best Stocks", command=self.update_best_stocks)
    self.button_best_stocks.pack()

    # Initialize variables
    self.symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'FB']
    self.start_date = '2020-01-01'
    self.end_date = '2020-12-31'
   
  def add_ticker(self):
    ticker = tk.simpledialog.askstring("Add Ticker", "Enter ticker symbol:")
    if ticker is not None:
      self.symbols.append(ticker)
      self.listbox_tickers.insert(tk.END, ticker)

  def remove_ticker(self):
    ticker = self.listbox_tickers.get(tk.ACTIVE)
    if ticker is not None:
      self.symbols.remove(ticker)
      self.listbox_tickers.delete(tk.ACTIVE)

  def update_tickers(self):
    self.listbox_tickers.delete(0, tk.END)
    for ticker in self.symbols:
      self.listbox_tickers.insert(tk.END, ticker)

  def update_best_stocks(self):
    self.listbox_best_stocks.delete(0, tk.END)
    best_stocks = self.get_best_stocks()
    for stock in best_stocks:
      self.listbox_best_stocks.insert(tk.END, stock)

  def start_trading(self):
    data = gather_data(self.symb
  def get_best_stocks(self):
    processed_data = preprocess_data(data)
    features = extract_features(processed_data, self.window_size)
    labels = []
    for symbol, df in features.items():
      labels.append(df['Returns'])
    labels = pd.concat(labels)
    model, scaler = train_model(features, labels)
    return self.predict_best_stocks(model, scaler, data)

  def predict_best_stocks(self, model, scaler, data):
    best_stocks = []
    for symbol, df in data.items():
      X = df[['SMA', 'EWMA', 'ROC', 'Sentiment']].values
      X = scaler.transform(X)
      y_pred = model.predict(X)
      returns = df['Returns'].values[-len(y_pred):]
      if np.mean(y_pred * returns) > 0:
        best_stocks.append(symbol)
    return best_stocks

def main():
  app = App()
  app.mainloop()

if __name__ == '__main__':
  main()
