### This file defines constants, default parameters, mapping between sectors and their representative stock tickers ###

# Defining a dictionary with the sectors and the thickers I want to include in the analysis: TICKERS_BY_SECTOR
TICKERS_BY_SECTOR = {
    "Technology": ["AAPL", "MSFT", "NVDA"],
    "Energy": ["XOM", "CVX"],
    "Healthcare": ["JNJ", "PFE"],
    "Financials": ["JPM", "BAC"],
    "Consumer": ["PG", "KO"],
}

# Fixing default parameters for data download
DEFAULT_PERIOD = "1y" 
DEFAULT_INTERVAL = "1d"
AUTO_ADJUST = True 

# Constant value for trading days per year
TRADING_DAYS_PER_YEAR = 252
