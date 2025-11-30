"""
Configuration module for the Market Pulse project.
This file defines global constrants used across the entire project.
"""
# Sector ETFs 
SECTOR_ETFS = {
    "Technology": "XLK",
    "Energy": "XLE",
    "Healthcare": "XLV",
    "Financials": "XLF",
    "Utilities": "XLU",
}

# Default configuration values
DEFAULT_PERIOD = "1y" 
DEFAULT_INTERVAL = "1d"
AUTO_ADJUST = True 
TRADING_DAYS_PER_YEAR = 252
RISK_FREE_ANNUAL = 0.02 
