from market_pulse.config import TICKERS_BY_SECTOR
from market_pulse.data import fetch_prices
from market_pulse.metrics import (
    compute_daily_returns,
    make_sector_returns,
    summarize_returns,
    correlation_matrix,
    save_table
)
from market_pulse.visualization import (
    plot_sector_mean,
    plot_sector_volatility,
    plot_sector_corr_heatmap
)

def main(): 
    tickers = [t for lst in TICKERS_BY_SECTOR.values() for t in lst]
    prices = fetch_prices(tickers, save_csv=True)
    print("Data downloaded and saved")

    rets_ticker = compute_daily_returns(prices)

    sector_rets = make_sector_returns(rets_ticker, TICKERS_BY_SECTOR)
    print("sector-level returns calculated")

    sector_summary = summarize_returns(sector_rets, annualize=True)
    sector_corr = correlation_matrix(sector_rets)
    print("Metrics calculated")

    save_table(sector_summary, "outputs/sector_summary.csv")
    save_table(sector_corr, "outputs/sector_corr.csv")

    plot_sector_mean(sector_summary, "outputs/sector_mean.png")
    plot_sector_volatility(sector_summary, "outputs/sector_volatility.png")
    plot_sector_corr_heatmap(sector_corr, "outputs/sector_corr_heatmap.png")

    print("Pipeline completed")

if __name__ == "__main__":
    main ()