"""
Streamlit dashboard for exploring sector ETF performance.

This app:
- downloads historical prices for sector ETFs from Yahoo Finance
- computes daily returns and annualised metrics (mean return, volatility, Sharpe)
- shows correlations and cumulative growth over time
- allows interactive control of period, frequency and risk-free rate
"""
# Imports
from pathlib import Path
import sys
import pandas as pd
import streamlit as st

# Make package imports work when running from scripts
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from market_pulse.config import (
    SECTOR_ETFS, 
    DEFAULT_PERIOD, 
    DEFAULT_INTERVAL, 
    AUTO_ADJUST, 
    TRADING_DAYS_PER_YEAR, 
    RISK_FREE_ANNUAL,
)
from market_pulse.data import fetch_prices
from market_pulse.metrics import (
    compute_daily_returns, 
    summarize_returns, 
    correlation_matrix,
)
from market_pulse.visualization import (
    plot_sector_mean, 
    plot_sector_volatility, 
    plot_sector_sharpe, 
    plot_sector_corr_heatmap, 
    plot_cumulative_returns,
)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Market Pulse (ETF)", layout="wide")

st.title("Market Pulse — Sector ETFs")
st.caption(
    "Explore sector performance, risk and correlation using Yahoo Finance data (Technology, Energy, Utilities, Healthcare and Financials).")

st.markdown(
"""
**What this app does**

- Downloads historical prices for sector ETFs from Yahoo Finance  
- Computes **annualised return**, **volatility** and **Sharpe ratio**  
- Shows **correlation** and the **cumulative growth** of 1€ over time  
"""
)

# --- Sidebar controls ---
st.sidebar.header("Controls")

# Choose ETFs (keys or tickers both ok)
default_etfs = list(SECTOR_ETFS.values())
etf_labels = {v: k for k, v in SECTOR_ETFS.items()}
all_etfs = default_etfs  # you can add more ETFs later if you like

selected = st.sidebar.multiselect(
    "Select sector ETFs",
    options=all_etfs,
    default=default_etfs,
    format_func=lambda t: f"{etf_labels.get(t, t)} ({t})"
)

# period selection
period = st.sidebar.selectbox(
    "Period", 
    ["1y", "2y", "3y", "5y"], 
    index=["1y","2y","3y","5y"].index(DEFAULT_PERIOD) 
    if DEFAULT_PERIOD in ["1y","2y","3y","5y"] 
    else 0
)

# interval selection (frequency of price data)
interval = st.sidebar.selectbox(
    "Interval", 
    ["1d", "1wk", "1mo"], 
    index=["1d","1wk","1mo"].index(DEFAULT_INTERVAL) 
        if DEFAULT_INTERVAL in ["1d","1wk","1mo"] 
        else 0
)

# risk_free slider
risk_free = st.sidebar.slider(
    "Risk-free rate (annual)", 
    0.0, 
    0.05, 
    float(RISK_FREE_ANNUAL),
    0.001
)

# save prices to checkbox
save_csv = st.sidebar.checkbox(
    "Save downloaded prices to data/", 
    value=True
)

st.sidebar.markdown("---")
st.sidebar.write("Trading days/year:", TRADING_DAYS_PER_YEAR)
st.sidebar.write("Auto-adjust:", AUTO_ADJUST)

if not selected:
    st.warning("Select at least one ETF to proceed.")
    st.stop()

# --- DATA ---
@st.cache_data(show_spinner=True, ttl=60*10)
def load_prices(etfs, period, interval, auto_adjust, save_csv):
    """Download ETF prices and cache the result.

    Args:
        etfs: List of ETF tickers (e.g. ["XLK", "XLE"]).
        period: Lookback window (e.g. "1y", "5y").
        interval: Data frequency ("1d", "1wk", "1mo").
        auto_adjust: Whether to use adjusted prices.
        save_csv: If True, save prices to data/etf_prices.csv.

    Returns:
        DataFrame of adjusted close prices (index=date, columns=tickers).
    """
    df = fetch_prices(
        etfs,
        period=period,
        interval=interval,
        auto_adjust=auto_adjust,
        save_csv=save_csv,
        fname="etf_prices.csv"
    )
    return df

with st.spinner("Downloading prices from Yahoo Finance…"):
    prices = load_prices(selected, period, interval, AUTO_ADJUST, save_csv)

st.subheader("Prices (adjusted close)")
st.dataframe(prices.tail())

#  --- METRICS ---
returns = compute_daily_returns(prices)
summary = summarize_returns(returns, risk_free_annual=risk_free)
corr = correlation_matrix(returns)

# Show summary table
st.subheader("Annualised Metrics")
st.caption("MeanReturn and Volatility are annualized (×252, ×√252). Sharpe uses the selected risk-free rate.")
st.dataframe(summary.style.format({"MeanReturn": "{:.2%}", "Volatility": "{:.2%}", "Sharpe": "{:.2f}"}))

# Small KPI cards
best_return_ticker = summary["MeanReturn"].idxmax()
best_return_value  = summary["MeanReturn"].max()

most_risky_ticker  = summary["Volatility"].idxmax()
most_risky_value   = summary["Volatility"].max()

best_sharpe_ticker = summary["Sharpe"].idxmax()
best_sharpe_value  = summary["Sharpe"].max()


c1, c2, c3 = st.columns(3)
c1.metric("Best return", 
          f"{best_return_ticker}", 
          f"{best_return_value:.1%}")
c2.metric("Highest volatility", 
          f"{most_risky_ticker}", 
          f"{most_risky_value:.1%}")
c3.metric("Best Sharpe", 
          f"{best_sharpe_ticker}", 
          f"{best_sharpe_value:.2f}")

#  --- PLOTS AND TABLES ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Summary charts", "Correlation", "Cumulative growth", "Prices", "Raw metrics"]
)

# --- TAB 1: Summary charts ---
with tab1:
    st.markdown("### Return, Volatility and Sharpe Ratio")

    fig = plot_sector_mean(summary)
    st.pyplot(fig)

    fig = plot_sector_volatility(summary)
    st.pyplot(fig)

    fig = plot_sector_sharpe(summary)
    st.pyplot(fig)

# --- TAB 2: Correlation ---
with tab2:
    st.markdown("### Correlation (Daily Returns)")
    fig = plot_sector_corr_heatmap(corr)
    st.pyplot(fig)

# --- TAB 3: Cumulative growth ---
with tab3:
    st.markdown("### Cumulative Growth of 1€")
    st.caption("How 1€ invested in each sector ETF evolves over time.")
    fig = plot_cumulative_returns(returns)
    st.pyplot(fig)

# --- TAB 4: Prices ---
with tab4:
    st.markdown("### Adjusted Close Prices (Last Rows)")
    st.dataframe(prices.tail())

# --- TAB 5: Raw metrics ---
with tab5:
    st.markdown("### Full Annualised Metrics")
    st.dataframe(
        summary.style.format(
            {
                "MeanReturn": "{:.2%}",
                "Volatility": "{:.2%}",
                "Sharpe": "{:.2f}",
            }
        )
    )

st.success("Done! Adjust parameters in the sidebar to explore different scenarios.")