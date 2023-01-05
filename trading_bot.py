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
   

    stock_data.plot(x=x, y=['Close', 'Prediction', 'Buying Point', 'Selling Point'], ax=ax, x_compat=True)

    # Add Matplotlib figure to Tkinter tab
    canvas = FigureCanvasTkAgg(figure, tab)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

# Create main window
window = tk.Tk()
window.title("Stock Predictor")
window.geometry("600x400")

# Create tab control
tab_control = ttk.Notebook(window)
tab_control.pack(expand=1, fill='both')

# Create input field for ticker
ticker_label = tk.Label(window, text="Ticker:")
ticker_label.pack()
ticker_entry = tk.Entry(window)
ticker_entry.pack()

# Create input field for percentage
percentage_label = tk.Label(window, text="Percentage:")
percentage_label.pack()
percentage_entry = tk.Spinbox(window, from_=0, to=100, increment=1)
percentage_entry.pack()

# Create button to add ticker to tab control
add_button = tk.Button(window, text="Add", command=lambda: create_tab(ticker_entry.get(), float(percentage_entry.get())))
add_button.pack()

window.mainloop()

