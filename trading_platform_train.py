#!/usr/bin/env python
import pandas as pd
df = pd.read_csv("USDCHF_Candlestick_4_Hour_ASK_05.05.2003-19.10.2019.csv")
df.tail()

#Check if any zero volumes are available
indexZeros = df[ df['volume'] == 0 ].index

df.drop(indexZeros , inplace=True)
df.loc[(df["volume"] == 0 )]
df.isna().sum()