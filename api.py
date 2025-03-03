from SmartApi import SmartConnect # Importing SmartConnect class from SmartApi
import pyotp  # Library for generating TOTP (Time-based One-Time Passwords)
from logzero import logger  # Logger for logging errors and messages
import pandas as pd  # Pandas library for handling dataframes
from constants import tokens  # Importing predefined tokens
from datetime import datetime, timedelta  # Importing datetime and timedelta for date manipulations
import time  # Importing time library

# API credentials for authentication
api_key = 'YOUR_API_KEY'
username = 'YOUR_USERNAME'
pwd = 'YOUR_PASSWORD'

# Initializing the SmartConnect API
smartApi = SmartConnect(api_key)

try:
    # Generate TOTP using a predefined token
    token = "YOUR_TOKEN"
    totp = pyotp.TOTP(token).now()
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")  # Logging error for invalid token
    raise e  # Raising exception if token is invalid

# Generating session using credentials
data = smartApi.generateSession(username, pwd, totp)

def lastMarketOpen():
    """Function to determine the last market open date"""
    today = datetime.now()
    last_open_date = today

    # Adjusting the last open date based on the current day
    if today.weekday() == 0:  # If today is Monday, last open date is Friday
        last_open_date -= timedelta(days=3)
    elif today.weekday() == 6:  # If today is Sunday, last open date is Friday
        last_open_date -= timedelta(days=2)
    elif today.weekday() == 5:  # If today is Saturday, last open date is Friday
        last_open_date -= timedelta(days=1)
    else:  # Any other weekday, last open date is previous day
        last_open_date -= timedelta(days=1)

    # Formatting the date to match required format
    return last_open_date.strftime("%Y-%m-%d 09:15")

def getData(symboltoken):
    """Function to fetch historical candle data for a given stock symbol"""
    params = {
        "exchange": "NSE",  # Exchange name (National Stock Exchange)
        "symboltoken": symboltoken,  # Symbol token for stock
        "interval": "FIFTEEN_MINUTE",  # Time interval for candles
        "fromdate": lastMarketOpen(),  # Fetching data from the last market open
        "todate": datetime.now().strftime("%Y-%m-%d %H:%M")  # Current date and time
    }

    # Fetching candle data from Smart API
    candle_data = smartApi.getCandleData(params)
    
    # Converting data into a pandas DataFrame
    df = pd.DataFrame(candle_data['data'], columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    
    # Converting 'close' column to numeric values
    df['close'] = pd.to_numeric(df['close'])
    
    # Calculating Exponential Moving Averages (EMA)
    df['EMA9'] = df['close'].ewm(span=9, adjust=False).mean()
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    
    return df  # Returning the dataframe

def check_ema_crossover(df):
    """Function to check for EMA crossover indicating a buy signal"""
    if len(df) < 5:
        return False  # Not enough data to analyze crossover

    recent_data = df.iloc[-5:]  # Extracting the last 5 rows for analysis
    
    # Checking if EMA9 is increasing
    ema_increasing = recent_data["EMA9"].is_monotonic_increasing
    if not ema_increasing:
        return False
    
    # Ensuring the first three EMAs are below EMA20
    for i in range(3):
        if recent_data["EMA9"].iloc[i] > recent_data["EMA20"].iloc[i]:
            return False
    
    # Checking if the last two EMAs indicate a crossover
    check_last = recent_data["EMA9"].iloc[4] >= recent_data["EMA20"].iloc[4]
    check_lastsecond = recent_data["EMA9"].iloc[3] >= recent_data["EMA20"].iloc[3]
    
    return check_last and check_lastsecond  # Returning True if crossover is confirmed

def placeOrder(symbol, token):
    """Function to place a market buy order"""
    order = {
        "variety": "NORMAL",  # Order type: NORMAL, AMO, STOPLOSS, etc.
        "tradingsymbol": f"{symbol}-EQ",  # Trading symbol of the stock
        "symboltoken": f"{token}",  # Symbol token from API
        "transactiontype": "BUY",  # BUY or SELL
        "exchange": "NSE",  # Exchange (NSE/BSE)
        "ordertype": "MARKET",  # Order type (LIMIT/MARKET/STOPLOSS)
        "producttype": "DELIVERY",  # Product type (DELIVERY/INTRADAY)
        "duration": "DAY",  # Duration (DAY/IOC)
        "quantity": 1,  # Number of shares to buy
    }
    try:
        order_id = smartApi.placeOrder(order)  # Placing order
        return order_id, True  # Returning order ID and success status
    except Exception as e:
        return "None", False  # Returning failure response if order placement fails