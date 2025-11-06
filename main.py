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
    plot_sector_sharpe
)

def main():
    # Definition of the ETFs to analyze
    etfs = list(SECTOR_ETFS.values())
    # Download data
    prices = fetch_prices(
        etfs,
        period=DEFAULT_PERIOD,
        interval=DEFAULT_INTERVAL,
        auto_adjust=AUTO_ADJUST,
        save_csv=True,
        fname="etf_prices.csv"
    )

    # Rename columns ETF->sector for nicer plots (XLK->Technology, ...)
    # prices = prices.rename(columns={v: k for k, v in SECTOR_ETFS.items()})

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

    print("ETF pipeline completed")

if __name__ == "__main__":
    main()