"""
Data loading utilities for the Market Pulse project.
The output of this module is useful to compute metrics and visualizations in the project.
"""

# Import libraries
from pathlib import Path
import yfinance as yf
import pandas as pd
from .config import DEFAULT_PERIOD, DEFAULT_INTERVAL, AUTO_ADJUST, SECTOR_ETFS


def fetch_prices(
    tickers,                             # List of ticker symbols
    period=DEFAULT_PERIOD,               # How far back to fetch data (1 year)
    interval=DEFAULT_INTERVAL,           # Frequency of observations (1 day)
    auto_adjust=AUTO_ADJUST,             # Automatically adjust prices for dividends/splits
    save_csv=True,                       # Whether to save data to CSV (default=yes)
    data_dir="data",                     # Directory where the CSV will be stored
    fname="prices.csv",                  # Output file name: prices.csv
) -> pd.DataFrame:                       # The function returns a pandas DataFrame
    """
    This function downloads ETF prices from Yahoo Finance and returns a price table.

    Prices are downloaded from Yahoo Finance via `yfinance.download`.
    Only the adjusted close prices are kept, and rows with missing values
    are dropped. Columns are renamed from ticker symbols to sector names
    using the `SECTOR_ETFS` mapping (if available).

    Args:
        tickers (list[str]): List of ticker symbols to download
        period (str): Lookback period for the download
        interval (str): Sampling frequency of the data
        auto_adjust (bool): Whether to auto-adjust prices for splits and dividends.
        save_csv (bool): If True, save the downloaded data to CSV.
        data_dir (str): Folder where the CSV will be written.
        fname (str): Name of the CSV file.

    Returns:
        pd.DataFrame: DataFrame of adjusted close prices, one column for each ETF.
    """

    print(f"Downloading: {', '.join(tickers)}")

    df = yf.download(
        tickers, period=period, interval=interval, auto_adjust=auto_adjust
    )["Close"].dropna()

    sector_names = {v: k for k, v in SECTOR_ETFS.items()}
    df = df.rename(columns=sector_names)
    
    # Save data to a CSV file
    if save_csv:
        p = Path(data_dir)
        p.mkdir(parents=True, exist_ok=True)
        out = p / fname
        df.to_csv(out)
        print(f"Saved {out}")
    return df