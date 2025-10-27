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

def save_table(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)
    print(f"saved:{path}")

## test to see if the .metrics.py code works. 
## run: python -m market_pulse.metrics

if __name__=="__main__":
    from market_pulse.config import TICKERS_BY_SECTOR
    from market_pulse.data import fetch_prices

    tickers = sum(TICKERS_BY_SECTOR.values(), [])  # flatten all sector tickers
    prices  = fetch_prices(tickers, save_csv=False)  # we only need in-memory here
    rets    = compute_daily_returns(prices)
    summary = summarize_returns(rets, annualize=True)
    corr    = correlation_matrix(rets)

    print("\nDaily returns (head):")
    print(rets.head())

    print("\nSummary stats:")
    print(summary)

    print("\nCorrelation matrix:")
    print(corr)

    save_table(summary, "outputs/summary_stats.csv")
    save_table(corr,    "outputs/correlation_matrix.csv")
