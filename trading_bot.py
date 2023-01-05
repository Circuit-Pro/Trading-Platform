import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import Frame, Button, Entry, Spinbox
from tkinter import filedialog
import tkinter.messagebox as messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to retrieve stock data and make predictions
def predict_stock(ticker, period):
    try:
        # Get stock data
        stock_data = yf.Ticker(ticker).history(period=str(period))
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return None

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
def create_tab(ticker, period, percentage):
    # Retrieve stock data and predictions. Validate stock data.
    try:
        stock_data = yf.Ticker(ticker).history(period=str(period))
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

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
window.geometry("600x400") # Make this window resizable,  minimize, and fullscreen capable.
# Create tab control
tab_control = ttk.Notebook(window)
tab_control.pack(expand=1, fill='both')

# Create input frame
input_frame = Frame(window)
input_frame.pack(side='top')

# Create prediction frame
prediction_frame = Frame(window)
prediction_frame.pack(side='top')

# Create buy frame
buy_frame = Frame(window)
buy_frame.pack(side='top')

# Create sell frame
sell_frame = Frame(window)
sell_frame.pack(side='top')

# Create buy button
buy_button = Button(buy_frame, text='Buy', command=lambda: buy_frame.destroy())
buy_button.pack()

# Create sell button
sell_button = Button(sell_frame, text='Sell', command=lambda: sell_frame.destroy())
sell_button.pack()

# Create prediction button
prediction_button = Button(prediction_frame, text='Predict', command=lambda: prediction_frame.destroy())
prediction_button.pack()

#Create period label and entry
period = StringVar()
period_label = tk.Label(window, text="Time Period : #y : #mo : ytd :max")
period_entry = tk.Entry(window)
period.set('1Y') # Default
period_label.pack()
period_entry.pack()

# Create percentage label and entry
percentage = StringVar()
percentage_label = tk.Label(input_frame, text="Percentage:")
percentage_entry = tk.Entry(input_frame, textvariable=percentage)
percentage.set('0.1') # Default
percentage_label.pack(side='left')
percentage_entry.pack(side='left')

# Create ticker label and entry
ticker_label = tk.Label(input_frame, text="Ticker:")
ticker_label.pack(side='left')
ticker_entry = tk.Entry(input_frame)
ticker_entry.pack(side='left')

#Create add button
add_button = tk.Button(window, text="Add", command=lambda: create_tab(ticker_entry.get(), period_entry.get(), float(percentage_entry.get())))
add_button.pack()

#Create quit button
quit_button = tk.Button(window, text="Quit", command=window.quit)
quit_button.pack()

#Run Tkinter event loop
window.mainloop()


