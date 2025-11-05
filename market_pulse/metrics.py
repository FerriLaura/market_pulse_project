from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252

# daily returns
def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    if not isinstance (prices, pd.DataFrame):
        raise TypeError("prices must be a padas DataFrame of Close prices")
    # percent daily returns
    return prices.pct_change().dropna()

<<<<<<< Updated upstream
def summarize_returns(
    returns: pd.DataFrame,
    annualize: bool = True,
    trading_days: int = TRADING_DAYS_PER_YEAR
=======
# annualize statistics
def annualize_stats(
        daily_mean: pd.Series,
        daily_std: pd.Series,
        periods_per_year: int = TRADING_DAYS_PER_YEAR,
):
    ann_mean = daily_mean * periods_per_year
    ann_std  = daily_std * np.sqrt(periods_per_year)
    return ann_mean, ann_std

# Share ratio
def sharpe_ratio(
        returns: pd.DataFrame,
        risk_free_annual: float = 0.02,
        periods_per_year: int = TRADING_DAYS_PER_YEAR
) -> pd.Series:
    mean_d = returns.mean()
    std_d  = returns.std(ddof=1)                 

    mu, sigma = annualize_stats(mean_d, std_d, periods_per_year)
    sigma = sigma.replace({0.0: np.nan})  # avoid division by zero

    sharpe = (mu - risk_free_annual) / sigma
    sharpe.name = "Sharpe"
    return sharpe

# Summary table with annualized MeanReturn, Volatility, Variance and Sharpe
def summarize_returns(
    returns: pd.DataFrame,
    annualize: bool = True,
    trading_days: int = TRADING_DAYS_PER_YEAR, 
    risk_free_annual: float = 0.02
>>>>>>> Stashed changes
) -> pd.DataFrame:
    if returns.empty:
        raise ValueError("returns is empty")
    
    mean_daily = returns.mean()
<<<<<<< Updated upstream
    vol_daily = returns.std()
    var_daily = vol_daily**2

    if annualize: 
        mean = mean_daily * trading_days
        vol = vol_daily * np.sqrt(trading_days)
        var = vol**2
=======
    vol_daily = returns.std(ddof=1)
    var_daily = vol_daily ** 2

    if annualize: 
        N = returns.shape[0]                    # number of trading days in sample
        growth = (1.0 + returns).prod()         # cumulative growth per column
        mean   = growth ** (trading_days / N) - 1   # 1-year equivalent (geometric)
        vol    = vol_daily * np.sqrt(trading_days)  # annualized volatility
        var    = vol ** 2
>>>>>>> Stashed changes
    else:
        mean, vol, var = mean_daily, vol_daily, var_daily
    
    out = pd.DataFrame({
        "MeanReturn": mean,
        "Volatility": vol,
        "Variance": var,
    })
<<<<<<< Updated upstream
=======

    out["Sharpe"] = sharpe_ratio(returns, risk_free_annual, trading_days)
>>>>>>> Stashed changes
    out.index.name = "Ticker"
    return out


# Correlation matrix across columns
def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.corr()

<<<<<<< Updated upstream
=======
# compute sector aggregation (equally weighted)
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
    sector_ret = pd.DataFrame(sector_cols)
    return sector_ret.dropna()

# Save any dataframe to CSV, creating parent folders if needed
def save_table(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)
    print(f"saved:{path}")

