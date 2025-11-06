# Import libraries
from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd
from .config import TRADING_DAYS_PER_YEAR, RISK_FREE_ANNUAL

# Compute daily returns 
def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    # Check that input is a pandas DataFrame 
    if not isinstance (prices, pd.DataFrame):
        raise TypeError("prices must be a padas DataFrame of Close prices")
    # percent daily returns -> formula: (P_t - P_{t-1}) / P_{t-1}
    # dropna() removes the first row (which is NaN after pct_change)
    return prices.pct_change().dropna()

# Summary table with annualized MeanReturn, Volatility and Sharpe ratio
def summarize_returns(
    returns: pd.DataFrame,
    trading_days: int = TRADING_DAYS_PER_YEAR,
    risk_free_annual: float = RISK_FREE_ANNUAL,
) -> pd.DataFrame:
    # Safety check: ensure data is not empty 
    if returns.empty:
        raise ValueError("returns is empty")

    # Compute daily statistics
    mean_d = returns.mean()         # average daily return
    vol_d = returns.std(ddof=1)     # sample std deviation 
    
    # Annualize: mean * 252; vol * sqrt(252)
    mean_a = mean_d * trading_days
    vol_a = vol_d * np.sqrt(trading_days)
   
    # Sharpe (risk-adjusted return); protect agaist division by zero
    sharpe = (mean_a - risk_free_annual) / vol_a.replace({0.0: np.nan})

    # Assemble the output table
    out = pd.DataFrame({
        "MeanReturn": mean_a,
        "Volatility": vol_a,
        "Sharpe": sharpe,
    })
    out.index.name = "Ticker"         
    return out


# Correlation matrix across columns
def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.corr()                 # Measures how columns move together: -1...+1

# Save any dataframe to CSV, creating parent folders if needed
def save_table(df: pd.DataFrame, path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)         # Ensure folder exists
    df.to_csv(p)                                        # Write CSV
    print(f"Saved: {p}")                                # Confirmation 