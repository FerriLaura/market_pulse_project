# Imports
from pathlib import Path
import sys
import pandas as pd
import streamlit as st

# Make package imports work when running from scripts
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from market_pulse.config import SECTOR_ETFS, DEFAULT_PERIOD, DEFAULT_INTERVAL, AUTO_ADJUST, TRADING_DAYS_PER_YEAR, RISK_FREE_ANNUAL
from market_pulse.data import fetch_prices
from market_pulse.metrics import compute_daily_returns, summarize_returns, correlation_matrix
from market_pulse.visualization import (
    plot_sector_mean, plot_sector_volatility, plot_sector_sharpe, plot_sector_corr_heatmap
)

st.set_page_config(page_title="Market Pulse (ETF)", layout="wide")

st.title("Market Pulse — Sector ETFs")
st.caption("Explore sector performance, risk and correlation using Yahoo Finance data (XLK, XLE, XLV).")

# Sidebar controls 
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

period = st.sidebar.selectbox("Period", ["1y", "2y", "3y", "5y"], index=["1y","2y","3y","5y"].index(DEFAULT_PERIOD) if DEFAULT_PERIOD in ["1y","2y","3y","5y"] else 0)
interval = st.sidebar.selectbox("Interval", ["1d", "1wk", "1mo"], index=["1d","1wk","1mo"].index(DEFAULT_INTERVAL) if DEFAULT_INTERVAL in ["1d","1wk","1mo"] else 0)
risk_free = st.sidebar.slider("Risk-free rate (annual)", 0.0, 0.05, float(RISK_FREE_ANNUAL), 0.001)

save_csv = st.sidebar.checkbox("Save downloaded prices to data/", value=True)

st.sidebar.markdown("---")
st.sidebar.write("Trading days/year:", TRADING_DAYS_PER_YEAR)
st.sidebar.write("Auto-adjust:", AUTO_ADJUST)

if not selected:
    st.warning("Select at least one ETF to proceed.")
    st.stop()

# DATA
@st.cache_data(show_spinner=True, ttl=60*10)
def load_prices(etfs, period, interval, auto_adjust, save_csv):
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

#  METRICS
returns = compute_daily_returns(prices)
summary = summarize_returns(returns, risk_free_annual=risk_free)
corr = correlation_matrix(returns)

# Show summary table
st.subheader("Annualized Metrics")
st.caption("MeanReturn and Volatility are annualized (×252, ×√252). Sharpe uses the selected risk-free rate.")
st.dataframe(summary.style.format({"MeanReturn": "{:.2%}", "Volatility": "{:.2%}", "Sharpe": "{:.2f}"}))

#  PLOTS 

# --- Sharpe Ratio ---
st.markdown("### Sharpe Ratio (Annual)")
fig = plot_sector_sharpe(summary)         # returns a Matplotlib Figure
st.pyplot(fig)                            # <- pass the fig

# --- Mean Return ---
st.markdown("### Mean Annual Return")
fig = plot_sector_mean(summary)
st.pyplot(fig)

# --- Volatility ---
st.markdown("### Volatility (Annual)")
fig = plot_sector_volatility(summary)
st.pyplot(fig)

# --- Correlation ---
st.markdown("### Correlation (Daily Returns)")
fig = plot_sector_corr_heatmap(corr)
st.pyplot(fig)


st.success("Done! Adjust parameters in the sidebar to explore different scenarios.")