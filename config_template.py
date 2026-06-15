# ============================================================
# StockVision — Configuration Template
# Copy this file to config.py and fill in your credentials.
# config.py is listed in .gitignore and will NOT be committed.
# ============================================================

DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "YOUR_MYSQL_PASSWORD",   # ← replace this
    "database": "stockvision"
}

START_DATE = "2010-01-01"
END_DATE   = "2024-12-31"

NIFTY_50 = [
    "TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS",
    "HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS",
    "SBIN.NS", "INDUSINDBK.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS",
    "HDFCLIFE.NS", "SBILIFE.NS", "SHRIRAMFIN.NS", "MARUTI.NS",
    "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS", "HEROMOTOCO.NS",
    "EICHERMOT.NS", "SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS",
    "DIVISLAB.NS", "APOLLOHOSP.NS", "RELIANCE.NS", "ONGC.NS",
    "BPCL.NS", "POWERGRID.NS", "NTPC.NS", "COALINDIA.NS",
    "HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS",
    "TATACONSUM.NS", "TATASTEEL.NS", "HINDALCO.NS", "JSWSTEEL.NS",
    "LT.NS", "ADANIPORTS.NS", "ADANIENT.NS", "ASIANPAINT.NS",
    "GRASIM.NS", "ULTRACEMCO.NS", "TITAN.NS", "BHARTIARTL.NS", "BEL.NS",
]

SP500_TOP30 = [
    "AAPL", "NVDA", "MSFT", "AVGO", "AMD", "ORCL", "CSCO", "CRM",
    "AMZN", "TSLA", "HD", "MCD", "COST", "GOOGL", "META", "NFLX",
    "JPM", "V", "MA", "BAC", "BRK-B", "LLY", "UNH", "JNJ",
    "ABT", "XOM", "CVX", "WMT", "PG", "CAT",
]

ALL_STOCKS = {"india": NIFTY_50, "us": SP500_TOP30}