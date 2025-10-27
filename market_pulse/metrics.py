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

def make_sector_returns(
    returns: pd.DataFrame,
    tickers_by_sector: dict[str, list[str]]
) -> pd.DataFrame:
    sector_cols = {}
    for sector, tickers in tickers_by_sector.items():
        cols = [t for t in tickers if t in returns.columns]
        if not cols: 
            continue
        sector_cols[sector] = returns[cols].mean(axis=1)
    sector_ret = pd.DataFrame(sector_cols)
    return sector_ret.dropna()

if __name__ == "__main__":
    from market_pulse.data import fetch_prices
    from market_pulse.config import TICKERS_BY_SECTOR

    # Download or load prices
    tickers = [t for lst in TICKERS_BY_SECTOR.values() for t in lst]
    prices = fetch_prices(tickers, save_csv=False)

    # Compute daily returns (ticker-level)
    rets_ticker = compute_daily_returns(prices)

    # Aggregate to sector-level
    sector_rets = make_sector_returns(rets_ticker, TICKERS_BY_SECTOR)
    print("\nSector returns (head):")
    print(sector_rets.head())

# Compute summary statistics and correlation for sectors
sector_summary = summarize_returns(sector_rets, annualize=True)
sector_corr = correlation_matrix(sector_rets)

print("\nSector summary stats:")
print(sector_summary)
print("\nSector correlation matrix:")
print(sector_corr)

save_table(sector_summary, "outputs/sector_summary.csv")
save_table(sector_corr, "outputs/sector_corr.csv")
