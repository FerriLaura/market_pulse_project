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

