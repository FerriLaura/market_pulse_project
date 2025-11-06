# Imports
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

# Utility to save or show plots (show on schreen or save it to file if a path is provided)
def _save_or_show(out_path: str | Path = None):
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True) # Ensure folder exists
        plt.savefig(out_path, bbox_inches="tight") # Save plot
        print(f"Saved plot: {out_path}")
    else:
        plt.show()              # Display the plot if it is not saved
    plt.close()                 # Clear figure from memory

# Generic helper for bar plots
def _bar_plot(
    df: pd.DataFrame,
    column: str,
    title: str,
    ylabel: str,
    color: str = "skyblue",
    out_path: str | Path = None,
):
    ax = df[column].sort_values(ascending=False).plot(
        kind="bar", figsize=(8, 5), color=color
    )
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Sector (ETF)")
    _save_or_show(out_path)

# Specific plots built using the function that I defined (_bar_plot)
# Bar plot of mean annual returns for each ETF
def plot_sector_mean(summary_df: pd.DataFrame, out_path: str | Path = None):
    _bar_plot(summary_df, "MeanReturn", "Mean Annual Return (ETFs)", "Return", "skyblue", out_path)

# Bar plot of annualized volatility for each ETF
def plot_sector_volatility(summary_df: pd.DataFrame, out_path: str | Path = None):
    _bar_plot(summary_df, "Volatility", "Annualized Volatility (ETFs)", "Volatility", "orange", out_path)

# Bar plot of Sharpe ratios for each ETF
def plot_sector_sharpe(summary_df: pd.DataFrame, out_path: str | Path = None):
    _bar_plot(summary_df, "Sharpe", "Sharpe Ratio (ETFs)", "Sharpe", "mediumseagreen", out_path)

# Heatmap showing pairwise correlations among ETFs
def plot_sector_corr_heatmap(corr_df: pd.DataFrame, out_path: str | Path = None):
    plt.figure(figsize=(5.5, 5))
    sns.heatmap(
        corr_df, annot=True, cmap="coolwarm",
        vmin=-1, vmax=1, square=True, fmt=".2f"
    )
    plt.title("Correlation Matrix (ETFs)")
    _save_or_show(out_path)