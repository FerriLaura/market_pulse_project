# Defining a dictionary with the sectors and the thickers I want to include in the analysis: TICKERS_BY_SECTOR

TICKERS_BY_SECTOR = {
    "Technology": ["AAPL", "MSFT", "NVDA"],
    "Energy": ["XOM", "CVX", "COP"],
    "Healthcare": ["JNJ", "PFE", "ABBV"],
}

# Default configuration values
DEFAULT_PERIOD = "5y" 
DEFAULT_INTERVAL = "1d"
AUTO_ADJUST = True 
TRADING_DAYS_PER_YEAR = 252
