from pathlib import Path
import yfinance as yf
import pandas as pd
from .config import DEFAULT_PERIOD, DEFAULT_INTERVAL, AUTO_ADJUST


def fetch_prices(
    tickers,
    period = DEFAULT_PERIOD,
    interval = DEFAULT_INTERVAL,
    auto_adjust = AUTO_ADJUST,
    save_csv = True,
    data_dir = "data",
    fname_prefix = "prices"
):

    print(f"Downloading data for: {', '.join(tickers)}")
    df = yf.download(
        tickers,
        period=period,
        interval=interval,
        auto_adjust=True
    )["Close"].dropna()

    if save_csv:
        data_path = Path(data_dir)
        data_path.mkdir(exist_ok=True)
        out = data_path / f"{fname_prefix}.csv"
        df.to_csv(out)
        print(f"saved data to {out}")

    return df

data = fetch_prices(["AAPL", "MSFT"])
print(data.head())

if __name__ == "__main__":
    from .config import TICKERS_BY_SECTOR
    fetch_prices(TICKERS_BY_SECTOR["Technology"])