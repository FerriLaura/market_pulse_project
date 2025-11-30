"""Main script to run the full ETF analysis pipeline.

This script executes the full workflow of the Market Pulse project:
- downloads ETF price data from Yahoo Finance
- computes daily returns
- calculates annualised performance and risk metrics
- generates correlation matrices
- saves all results to CSV files
- generates and exports all visualizations

Running this file produces the complete set of outputs under /outputs/.
"""

# Imports
from market_pulse.config import SECTOR_ETFS, DEFAULT_PERIOD, DEFAULT_INTERVAL, AUTO_ADJUST, RISK_FREE_ANNUAL
from market_pulse.data import fetch_prices
from market_pulse.metrics import (
    compute_daily_returns,
    summarize_returns,
    correlation_matrix,
    save_table
)
from market_pulse.visualization import (
    plot_sector_mean,
    plot_sector_volatility,
    plot_sector_corr_heatmap,
    plot_sector_sharpe,
    plot_cumulative_returns
)

def main():
    """Run the full sector ETF analysis pipeline.

    Steps:
        1. Select ETFs defined in config.py.
        2. Download adjusted close prices.
        3. Compute daily returns.
        4. Compute annualised mean return, volatility, and Sharpe ratio.
        5. Compute correlation matrix.
        6. Save results as CSV files.
        7. Generate all plots and save them to /outputs/.

    All outputs are saved automatically. No return value.
    """
    # definition of the ETFs to analyze
    etfs = list(SECTOR_ETFS.values())
    
    # download ETF price data
    prices = fetch_prices(
        etfs,
        period=DEFAULT_PERIOD,
        interval=DEFAULT_INTERVAL,
        auto_adjust=AUTO_ADJUST,
        save_csv=True,
        fname="etf_prices.csv"
    )

    # Compute daily returns
    returns    = compute_daily_returns(prices)
    
    # Compute summary metrics
    summary = summarize_returns(returns, risk_free_annual=RISK_FREE_ANNUAL)
    corr    = correlation_matrix(returns)

    # Save results
    save_table(summary, "outputs/sector_summary_etf.csv")
    save_table(corr,    "outputs/sector_corr_etf.csv")

    # Create visualizations
    plot_sector_mean(summary,        "outputs/sector_mean_etf.png")
    plot_sector_volatility(summary,  "outputs/sector_volatility_etf.png")
    plot_sector_sharpe(summary,      "outputs/sector_sharpe_etf.png")
    plot_sector_corr_heatmap(corr,   "outputs/sector_corr_heatmap_etf.png")
    plot_cumulative_returns(returns, "outputs/sector_cumulative_returns.png")

    print("ETF pipeline completed")

if __name__ == "__main__":
    main()