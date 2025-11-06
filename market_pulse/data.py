# Import libraries
from pathlib import Path
import yfinance as yf
import pandas as pd
from .config import DEFAULT_PERIOD, DEFAULT_INTERVAL, AUTO_ADJUST

# Function to download price data from Yahoo Finance
def fetch_prices(
    tickers,                             # List of ticker symbols
    period=DEFAULT_PERIOD,               # How far back to fetch data (1 year)
    interval=DEFAULT_INTERVAL,           # Frequency of observations (1 day)
    auto_adjust=AUTO_ADJUST,             # Automatically adjust prices for dividends/splits
    save_csv=True,                       # Whether to save data to CSV (default=yes)
    data_dir="data",                     # Directory where the CSV will be stored
    fname="prices.csv",                  # Output file name: prices.csv
) -> pd.DataFrame:                       # The function returns a pandas DataFrame
    
    # Print a message to show which tickers are being downloaded
    print(f"Downloading: {', '.join(tickers)}")

    # Download data using yfinance (we keep only the "Close" prices and drop rows with missing values)
    df = yf.download(
        tickers, period=period, interval=interval, auto_adjust=auto_adjust
    )["Close"].dropna()

    # Save data to a CSV file
    if save_csv:
        # Create the target directory if it doesn't exist
        p = Path(data_dir)
        p.mkdir(parents=True, exist_ok=True)
        # Define the full output file path
        out = p / fname
        # Save the DataFrame to CSV format
        df.to_csv(out)
        # Confirm that the file was saved and where
        print(f"Saved {out}")
    # Return the DataFrame for further analysis
    return df