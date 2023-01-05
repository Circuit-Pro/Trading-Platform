import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import ttk
from tkinter import Frame, Button, Entry, messagebox, Spinbox
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to retrieve stock data and make predictions
def predict_stock(ticker, period):
    # Get stock data
    stock_data = yf.Ticker(ticker).history(period=period)

    # Convert stock data to numpy array
    X = np.array(range(len(stock_data))).reshape(-1, 1)
    y = np.array(stock_data['Close']).reshape(-1, 1)

    # Fit linear regression model
    model = LinearRegression().fit(X, y)

    # Make predictions
    predictions = model.predict(X)

    # Add predictions to stock data
    stock_data['Prediction'] = predictions

    return stock_data


# Function to create tab for stock
def create_tab(ticker, percentage, period):
    # Retrieve stock data and predictions
    stock_data = predict_stock(ticker, period)

    # Add buying and selling points to stock data
    stock_data['Buying Point'] = stock_data['Close'].shift(1) * (1 + percentage/100)
    stock_data['Selling Point'] = stock_data['Close'].shift(1) * (1 - percentage/100)

    # Create tab for stock
    tab = Frame(tab_control)
    tab_control.add(tab, text=ticker)

    # Create Matplotlib figure and axes
    figure = plt.figure()
    ax = figure.add_subplot(111)

    # Add stock data to tab
    stock_data.plot(x='Date', y=['Close', 'Prediction', 'Buying Point', 'Selling Point'], ax=ax)

    # Add Matplotlib figure to Tkinter tab
    canvas = FigureCanvasTkAgg(figure, tab)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

# Create main window
window = tk.Tk()
window.title("Stock Predictor")
window.geometry("600x400") # Make this window resizeable, minamizeable, and fullscreen capeable.

# Create tab control
tab_control = ttk.Notebook(window)
tab_control.pack(expand=1, fill='both')

# Create input frame
input_frame = Frame(window)
input_frame.pack(side='top')

# Create ticker label and entry
ticker_label = tk.Label(input_frame, text="Ticker:")
ticker_label.pack(side='left')
ticker_entry = tk.Entry(input_frame)
ticker_entry.pack(side='left')

# Create percentage label and entry

percentage_label = tk.Label(window, text="Percentage:")
percentage_entry = tk.Entry(window)
if percentage_entry is None:
    percentage_entry = 0.01 # Default?
percentage_label.pack()
percentage_entry.pack()

#Create period label and entry

period_label = tk.Label(window, text="Time Period : YTD")
period_entry = tk.Entry(window)
if period_entry is None:
    period_entry = '1Y' # 1 YTD Default
period_label.pack()
period_entry.pack()

#Create add button

add_button = tk.Button(window, text="Add", command=lambda: create_tab(ticker_entry.get(), float(percentage_entry.get()), period_entry.get()))
add_button.pack()

#Create quit button

quit_button = tk.Button(window, text="Quit", command=window.quit)
quit_button.pack()

#Run Tkinter event loop

window.mainloop()


