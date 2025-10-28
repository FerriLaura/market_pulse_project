from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252

def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    if not isinstance (prices, pd.DataFrame):
        raise TypeError("prices must be a padas DataFrame of Close prices")
    return prices.pct_change().dropna()

def summarize_returns(
    returns: pd.DataFrame,
    annualize: bool = True,
    trading_days: int = TRADING_DAYS_PER_YEAR
) -> pd.DataFrame:
    mean_daily = returns.mean()
    vol_daily = returns.std()
    var_daily = vol_daily**2

    if annualize: 
        mean = mean_daily * trading_days
        vol = vol_daily * np.sqrt(trading_days)
        var = vol**2
    else:
        mean, vol, var = mean_daily, vol_daily, var_daily

    out = pd.DataFrame({
        "MeanReturn": mean,
        "Volatility": vol,
        "Variance": var
    })
    out.index.name = "Ticker"
    return out

def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.corr()

def make_sector_returns(
    returns: pd.DataFrame,
    tickers_by_sector: dict[str, list[str]],
) -> pd.DataFrame:
    sector_cols = {}
    for sector, tickers in tickers_by_sector.items():
        cols = [t for t in tickers if t in returns.columns]
        if not cols:
            print(f"No tickers found for sector: {sector}")
            continue
        sector_cols[sector] = returns[cols].mean(axis=1)
    sector_ret = pd.DataFrame(sector_cols)
    return sector_ret.dropna()

def save_table(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)
    print(f"saved:{path}")

