import pandas as pd
import yfinance as yf
import numpy as np
from yahoofinancials import YahooFinancials
import yahooquery as yq
import matplotlib
from matplotlib import pyplot as plt

def moving_average(data, window):
    return np.convolve(data, np.ones(window), 'valid') / window

def base_invest(ticker):
    # Get ticker's stock data
    ticker_df = ticker.history(period="20y")
    
    # Filter Data
    order = (int)(ticker_df['Close'].max() - ticker_df['Close'].min())
    ticker_filtered = moving_average(ticker_df['Close'], order)
    
    # Calclate stock velocity
    ticker_velocity = np.gradient(ticker_filtered)
    ticker_velocity_filtered = moving_average(ticker_velocity, order)
    
    # Calculate stock acceleration
    ticker_acceleration = np.gradient(ticker_velocity_filtered)
    ticker_acceleration_filtered = moving_average(ticker_acceleration, order)
    
    # Plot Stock Data
    ticker_dates = np.linspace(2003, 2023, ticker_filtered.size)
    plt.plot(ticker_dates, ticker_filtered)
    plt.show()
    
    velocity_dates = np.linspace(2003, 2023, ticker_velocity_filtered.size)
    plt.plot(velocity_dates, ticker_velocity_filtered
    plt.show()
    
    acceleration_dates = np.linspace(2003, 2023, ticker_acceleration_filtered.size)
    plt.plot(acceleration_dates, ticker_acceleration_filtered)
    plt.show()
    
    # Find standard deviation of velocity and acceleration
    velocity_std = np.std(ticker_velocity_filtered)
    acceleration_std = np.std(ticker_acceleration_filtered)
    
    # Print stock metrics
    print("Acceleration std: ", acceleration_std)
    print("Acceleration: ", ticker_acceleration_filtered[-1])
    print("Max Price: ", ticker_filtered.max())
    print("Stock Price: ", ticker_filtered[-1])
    
    # If stock is at maxima, sell. If stock is at minima, buy. Otherwise, hold.
    if (ticker_acceleration_filtered[-1] < -acceleration_std and ticker_filtered[-1] > ticker_filtered.max()):
        return "sell"
    elif (ticker_acceleration_filtered[-1] < -acceleration_std and ticker_filtered[-1] < ticker_filtered.min()):
        return "buy"
    else:
        return "hold"

def income_invest(ticker):
    # Get market cap from Yahoo Financials
    yh_ticker = YahooFinancials(ticker.ticker)
    market_cap = yh_ticker.get_market_cap()
    
    # Print Market Cap and Beta
    print("Market Cap: ", market_cap)
    print("Beta: ", ticker.info['beta'])
    
    # Weed out companies with high volatility and low market cap
    if (ticker.info['beta'] > 1.4 or market_cap < 50000000000):
        return "sell"
    
    return base_invest(ticker)

def growth_invest(ticker):   
    # Print Market Cap and Beta
    print("Revenue Growth: ", ticker.info['revenueGrowth'])
    
    #Weed out companies with low growth
    if (ticker.info['revenueGrowth'] < 0):
        return "sell"
    
    return base_invest(ticker)

def esg_invest(ticker):
    # Attempt to retrieve ESG Data
    try: 
        print("ESG: ", ticker.sustainability['totalEsg'])
        
        # Weed out companies with low ESG
        if (ticker.sustainability['totalEsg'] < 50):
            return "sell"
    except:
        print("Unable to get ESG due to decryption error")
        
    return base_invest(ticker)

def invest(ticker, client=False):
    if (client == "income"):
        return income_invest(ticker)
    elif (client == "growth"):
        return growth_invest(ticker)
    elif (client == "esg"):
        return esg_invest(ticker)
    else:
        return base_invest(ticker)
