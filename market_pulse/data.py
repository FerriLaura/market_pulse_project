from pathlib import Path
import yfinance as yf
import pandas as pd
from .config import DEFAULT_PERIOD, DEFAULT_INTERVAL, AUTO_ADJUST

def fetch_prices(
    tickers,
    period=DEFAULT_PERIOD,
    interval=DEFAULT_INTERVAL,
    auto_adjust=AUTO_ADJUST,
    save_csv=True,
    data_dir="data",
    fname="prices.csv",
) -> pd.DataFrame:
    print(f"Downloading: {', '.join(tickers)}")
    df = yf.download(
        tickers, period=period, interval=interval, auto_adjust=auto_adjust
    )["Close"].dropna()
    if save_csv:
        p = Path(data_dir); p.mkdir(parents=True, exist_ok=True)
        out = p / fname
        df.to_csv(out)
        print(f"Saved {out}")
    return df