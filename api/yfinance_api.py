#!/usr/bin/env python
import yfinance as yf
tickers = {"MSFT", "GOOGL"}

for ticker in tickers:
        tick = yf.Ticker(ticker)
        # get stock info
        def info():
            return tick.info

        def historical(period):
            # get historical market data
            return tick.history(period)

        def historical_metadata():
            # show meta information about the history (requires history() to be called first)
            historical()
            return tick.history_metadata

        def actions():
            # show actions (dividends, splits, capital gains)
            return tick.actions

        def dividends(): 
            # show dividends
            return tick.dividends

        def splits():
            # show splits
            return tick.splits

        def capital_gains():
            # show capital gains (for mutual funds & etfs)
            return tick.capital_gains

        def shares():
        # show share count
            return tick.shares

    # show financials:
        def income_statement(param): #True: entire stmt False: quarterly stmt
    # - income statement
            if param == True:
                return tick.income_stmt
            else:
                return tick.quarterly_income_stmt
    # - balance sheet
        def balance_sheet(param): #True: whole sheet False: quarterly sheet
            if param == True:
                return tick.balance_sheet
            else:
                return tick.quarterly_balance_sheet

        # - cash flow statement
        def cash_flow_statement(param): #True: entire stmt False: quarterly stmt
        # - cash flow
            if param == True:
                return tick.cashflow
            else:
                return tick.quarterly_cashflow
        # see `Ticker.get_income_stmt()` for more options

        def major_holders():
            # show major holders
            return tick.major_holders

        def institu_holders():    
            # show institutional holders
            return tick.institutional_holders

        def mutualfund_holders():    
        # show mutualfund holders
           return tick.mutualfund_holders

        def show_earnings(param):  
            # show earnings
            if param == True:
                return tick.earnings
            else:
                return tick.quarterly_earnings

        def sustainability():
            # show sustainability
            return tick.sustainability

        def analysts_rec(param):
            # show analysts recommendations
            if param == True:
                return tick.recommendations
            else:
                return tick.recommendations_summary

        # show analysts other work
        def analysts_other_work(param):
            # show analysts other work
            if param == 1:
                return tick.analyst_price_target
            elif param == 2:
                return tick.revenue_forecasts
            elif param == 3:
                return tick.earnings_forecasts
            else:
                return tick.earnings_trend


        def calendar():
            # show next event (earnings, etc)
            return tick.calendar

# Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default. 
# Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
        def earnings_dates():
            return tick.earnings_dates

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
        def isin():
            return tick.isin

# show options expirations
        def options_expirations():
            return tick.options

# show news
        def news():
            return tick.news


# get option chain for specific expiration
        #opt = tick.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts