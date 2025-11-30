# metrics.py
"""
Functions for computing daily returns, annualised metrics, and correlations
for sector ETF price data. These utilities are used throughout the project
to generate the performance and risk statistics shown in the analysis and
Streamlit dashboard.
"""

# Import libraries
from pathlib import Path
import numpy as np
import pandas as pd
from .config import TRADING_DAYS_PER_YEAR, RISK_FREE_ANNUAL


def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily percentage returns from a DataFrame of prices.
    
    Daily returns are calculated using the formula:
        (P_t - P_{t-1}) / P_{t-1}

    Args:
        prices (pd.DataFrame): DataFrame of adjusted close prices, where each
            column corresponds to an ETF.

    Returns:
        pd.DataFrame: Daily returns for each ETF. The first row is dropped
        because pct_change() produces a NaN in the first position.
    """
    if not isinstance (prices, pd.DataFrame):
        raise TypeError("prices must be a padas DataFrame of Close prices")
    
    return prices.pct_change().dropna()


def summarize_returns(
    returns: pd.DataFrame,
    trading_days: int = TRADING_DAYS_PER_YEAR,
    risk_free_annual: float = RISK_FREE_ANNUAL,
) -> pd.DataFrame:
    """
    Compute annualised mean return, volatility and Sharpe ratio.
    
    Daily mean and standard deviation are annualised using:
        mean * N_days
        std * sqrt(N_days)

    Args:
        returns (pd.DataFrame): Daily returns for each ETF.
        trading_days (int): Number of trading days used for annualisation.
        risk_free_annual (float): Annual risk-free rate used for Sharpe ratio.

    Returns:
        pd.DataFrame: Table with columns:
            - MeanReturn
            - Volatility
            - Sharpe
    """
    if returns.empty:
        raise ValueError("returns is empty")

    # Daily statistics
    mean_d = returns.mean()         
    vol_d = returns.std(ddof=1)     
    
    
    # Annualize
    mean_a = mean_d * trading_days
    vol_a = vol_d * np.sqrt(trading_days)
   
    # Sharpe 
    sharpe = (mean_a - risk_free_annual) / vol_a.replace({0.0: np.nan})

    
    out = pd.DataFrame({
        "MeanReturn": mean_a,
        "Volatility": vol_a,
        "Sharpe": sharpe,
    })
    out.index.name = "Ticker"         
    return out


# Correlation matrix 
def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Compute pairwise correlations between ETF returns.

    Args:
        returns (pd.DataFrame): Daily returns for each ETF.

    Returns:
        pd.DataFrame: Correlation matrix (values between -1 and 1).
    """
    return returns.corr()                 

# Save tables
def save_table(df: pd.DataFrame, path: str | Path) -> None:
    """
    Save a DataFrame to CSV, ensuring that folders are created if needed.

    Args:
        df (pd.DataFrame): Table to be saved.
        path (str | Path): Output file path for the CSV file.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)         
    df.to_csv(p)                                        
    print(f"Saved: {p}")                               