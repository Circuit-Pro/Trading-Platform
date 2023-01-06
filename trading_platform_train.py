#!/usr/bin/env python
import pandas as pd
import numpy as np
import pandas_ta as ta
from scipy.stats import linregress
from os import getcwd
import joblib
from tqdm import tqdm

# Analysis Example libraries
import matplotlib.pyplot as plt
from matplotlib import pyplot
from xgboost import plot_importance

# Model Libraries
#from sklearn.model_selection import train_test_split
#from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
total_steps = 15
with tqdm(total=total_steps, desc="% Loading % ", smoothing=True, unit="%") as pbar:
    print("! Loading Data Set !")
    pbar.update(1)  # update progress bar manually
    df = pd.read_csv(getcwd() + '/Trading-Platform/Dataset/set.csv')
    df.tail()

    #Check if any zero volumes are available
    indexZeros = df[ df['Volume'] == 0 ].index

    df.drop(indexZeros , inplace=True)
    df.loc[(df["Volume"] == 0 )]
    df.isna().sum()

    #df.ta.indicators()
    #help(ta.atr)
    df['ATR'] = df.ta.atr(length=20)
    df['RSI'] = df.ta.rsi()
    df['Average'] = df.ta.midprice(length=1) #midprice
    df['MA40'] = df.ta.sma(length=40)
    df['MA80'] = df.ta.sma(length=80)
    df['MA160'] = df.ta.sma(length=160)

    print("# Calculating Slopes #")
    pbar.update(1)  # update progress bar manually
    def get_slope(array):
        y = np.array(array)
        x = np.arange(len(y))
        slope, intercept, r_value, p_value, std_err = linregress(x,y)
        return slope

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    backrollingN = 6
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    df['slopeMA40'] = df['MA40'].rolling(window=backrollingN).apply(get_slope, raw=True)
    df['slopeMA80'] = df['MA80'].rolling(window=backrollingN).apply(get_slope, raw=True)
    df['slopeMA160'] = df['MA160'].rolling(window=backrollingN).apply(get_slope, raw=True)
    df['AverageSlope'] = df['Average'].rolling(window=backrollingN).apply(get_slope, raw=True)
    df['RSISlope'] = df['RSI'].rolling(window=backrollingN).apply(get_slope, raw=True)

    df.tail()

    #Target flexible way
    pipdiff = 500*1e-5 #for TP
    SLTPRatio = 2 #pipdiff/Ratio gives SL

    print("* Getting Target *")
    pbar.update(1)  # update progress bar manually
    def mytarget(barsupfront, df1):
        length = len(df1)
        high = list(df1['High'])
        low = list(df1['Low'])
        close = list(df1['Close'])
        open = list(df1['Open'])
        trendcat = [None] * length

        for line in range (0,length-barsupfront-2):
            valueOpenLow = 0
            valueOpenHigh = 0
            for i in range(1,barsupfront+2):
                value1 = open[line+1]-low[line+i]
                value2 = open[line+1]-high[line+i]
                valueOpenLow = max(value1, valueOpenLow)
                valueOpenHigh = min(value2, valueOpenHigh)

                if ( (valueOpenLow >= pipdiff) and (-valueOpenHigh <= (pipdiff/SLTPRatio)) ):
                    trendcat[line] = 1 #-1 downtrend
                    break
                elif ( (valueOpenLow <= (pipdiff/SLTPRatio)) and (-valueOpenHigh >= pipdiff) ):
                    trendcat[line] = 2 # uptrend
                    break
                else:
                    trendcat[line] = 0 # no clear trend
                
            return trendcat

        print("@ ^--^ @ Target Found in Data Frame @ ^--^ @")
        pbar.update(1)  # update progress bar manually
        # mytarget(barsfront to take into account, dataframe)
        df['mytarget'] = mytarget(16, df)
        df.head()

        print("!***! Anaylsis of Target !***!")
        pbar.update(1)  # update progress bar manually
        # Analysis example 
        fig = plt.figure(figsize = (8.9,8.9))
        ax = fig.gca()
        df_model= df[['Volume', 'ATR', 'RSI', 'Average', 'MA40', 'MA80', 'MA160', 'slopeMA40', 'slopeMA80', 'slopeMA160', 'AverageSlope', 'RSISlope', 'mytarget']] 
        df_model.hist(ax = ax)
        plt.show() # Kind of obnoctious...

        print("#*#*#* Splitting Features and Targets *#*#")
        pbar.update(1)  # update progress bar manually
        # Splitting Features and targets
        df_model=df_model.dropna()

        attributes=['ATR', 'RSI', 'Average', 'MA40', 'MA80', 'MA160', 'slopeMA40', 'slopeMA80', 'slopeMA160', 'AverageSlope', 'RSISlope']
        X = df_model[attributes]
        y = df_model["mytarget"]

        print(X)
        pbar.update(1)  # update progress bar manually

        # Finally Training the Model

        #random sampling - sloppier
        #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

        #sequential sampling
        print("@---@ Sequential Sampling @---@")
        pbar.update(1)  # update progress bar manually
        train_index = int(0.8 * len(X))
        X_train, X_test = X[:train_index], X[train_index:]
        y_train, y_test = y[:train_index], y[train_index:]

        # Training the Model
        print("!#@^*$ Training $*^@#!")
        pbar.update(1)  # update progress bar manually
        model = XGBClassifier()
        model.fit(X_train, y_train)
        pred_train = model.predict(X_train)
        pred_test = model.predict(X_test)

        # Accuracy/Sanity check
        print("<------% Sanity Check  %----->")
        pbar.update(1)  # update progress bar manually
        acc_train = accuracy_score(y_train, pred_train)
        acc_test = accuracy_score(y_test, pred_test)
        print('****Train Results****')
        pbar.update(1)  # update progress bar manually
        print("Accuracy: {:.4%}".format(acc_train))
        print('****Test Results****')
        pbar.update(1)  # update progress bar manually
        print("Accuracy: {:.4%}".format(acc_test))

        # Random Model, gambler?
        pred_test = np.random.choice([0, 1, 2], len(pred_test))
        accuracy_test = accuracy_score(y_test, pred_test)
        print("Accuracy Gambler: %.2f%%" % (accuracy_test * 100.0))
        pbar.update(1)  # update progress bar manually

        #plot feature importance
        print("!---! Plotting Feature Importance !---!")
        pbar.update(1)  # update progress bar manually
        plot_importance(model)
        pyplot.show()

        # RSI Alone as Trend indicator
        print("!***! Anaylsis of RSI Trend indicator !***!")
        pbar.update(1)  # update progress bar manually
        df_up=df.RSI[ df['mytarget'] == 2 ]
        df_down=df.RSI[ df['mytarget'] == 1 ]
        df_unclear=df.RSI[ df['mytarget'] == 0 ]
        pyplot.hist(df_unclear, bins=100, alpha=0.5, label='unclear')
        pyplot.hist(df_down, bins=100, alpha=0.5, label='down')
        pyplot.hist(df_up, bins=100, alpha=0.5, label='up')

        pyplot.legend(loc='upper right')
        pyplot.show()

        # Save ML model to disk
        print("!***! Saving ML Model to disk!***!")
        try:
            filename = getcwd() + '/Trading-Platform/Models/model.onyx'
            joblib.dump(model, filename)
            print("Success! ML Model saved to disk")
        except:
            print("Failed to save ML Model to disk")

