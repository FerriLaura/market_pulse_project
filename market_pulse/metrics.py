from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd
import yfinance as yf

TRADING_DAYS_PER_YEAR = 252

def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    if not isinstance (prices, pd.DataFrame):
        raise TypeError("prices must be a padas DataFrame of Close prices")
    return prices.pct_change().dropna()

def annualize_stats(daily_mean: pd.Series,
                    daily_std: pd.Series,
                    periods_per_year: int = TRADING_DAYS_PER_YEAR):
    ann_mean = daily_mean * periods_per_year
    ann_std  = daily_std * np.sqrt(periods_per_year)
    return ann_mean, ann_std

def sharpe_ratio(
        returns: pd.DataFrame,
        risk_free_annual: float = 2.0,
        periods_per_year: int = TRADING_DAYS_PER_YEAR
) -> pd.Series:
    mean_d = returns.mean()
    std_d  = returns.std()                 

    mu, sigma = annualize_stats(mean_d, std_d, periods_per_year)

    # avoid division by zero
    sigma = sigma.replace({0.0: np.nan})
    sharpe = (mu - risk_free_annual) / sigma
    sharpe.name = "Sharpe"
    return sharpe


def summarize_returns(
    returns: pd.DataFrame,
    annualize: bool = True,
    trading_days: int = TRADING_DAYS_PER_YEAR, 
    risk_free_annual: float = 0.2
) -> pd.DataFrame:
    mean_daily = returns.mean()
    vol_daily = returns.std()
    var_daily = vol_daily ** 2
    N = len(returns)  # number of trading days in the sample

    if annualize:
        N = returns.shape[0]  
        growth = (1 + returns).prod()        
        mean = growth ** (252 / N) - 1       

        vol = vol_daily * np.sqrt(trading_days)
        var = vol ** 2
    else:
        mean, vol, var = mean_daily, vol_daily, var_daily

    out = pd.DataFrame({
        "MeanReturn": mean,
        "Volatility": vol,
        "Variance": var
    })

    # sharpe uses annualized mean/vol internally; rf=0.02
    sharpe = sharpe_ratio(returns, risk_free_annual, trading_days)
    out["Sharpe"] = sharpe

    out.index.name = "Ticker"
    return out

def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.corr()

## compute sector returns equally weighted
# def make_sector_returns(
    #returns: pd.DataFrame,
    #tickers_by_sector: dict[str, list[str]],
#) -> pd.DataFrame:
    #sector_cols = {}
    #for sector, tickers in tickers_by_sector.items():
        #cols = [t for t in tickers if t in returns.columns]
        #if not cols:
            #print(f"No tickers found for sector: {sector}")
            #continue
        #sector_cols[sector] = returns[cols].mean(axis=1)
    #sector_ret = pd.DataFrame(sector_cols)
    #return sector_ret.dropna()

## compute sector returns weighted by sector capitalization
def make_sector_returns_weighted(returns: pd.DataFrame, tickers_by_sector: dict[str, list[str]]) -> pd.DataFrame:
    sector_cols = {}
    for sector, tickers in tickers_by_sector.items():
        valid_tickers = [t for t in tickers if t in returns.columns]
        if not valid_tickers:
            continue
        # fetch market caps (latest)
        tickers_info = {t: yf.Ticker(t).info.get("marketCap", None) for t in valid_tickers}
        tickers_info = {t: cap for t, cap in tickers_info.items() if cap is not None}
        # compute normalized weights
        total_cap = sum(tickers_info.values())
        weights = {t: cap / total_cap for t, cap in tickers_info.items()}
        # weighted average across tickers (row-wise)
        weighted_return = sum(returns[t] * weights[t] for t in weights)
        sector_cols[sector] = weighted_return

    return pd.DataFrame(sector_cols).dropna()

def save_table(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)
    print(f"saved:{path}")

