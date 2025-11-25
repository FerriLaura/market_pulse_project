# Imports
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

# Utility to save or show plots (show on schreen or save it to file if a path is provided)
def _maybe_save(fig, out_path: str | Path | None) -> None:
    """
    Save the Matplotlib figure to 'out_path' if not None.
    Does nothing if out_path is None.
    """
    if out_path:
        out_path = Path(out_path)
        Path(out_path).parent.mkdir(parents=True, exist_ok=True) # Ensure folder exists
        fig.savefig(out_path, bbox_inches="tight") # Save plot
        print(f"Saved plot: {out_path}")


# Generic helper for bar plots
def _bar_plot(
    df: pd.DataFrame,
    column: str,
    title: str,
    ylabel: str,
    color: str = "skyblue",
    out_path: str | Path = None,
):
    """
    Create a bar chart for a single column of a DataFrame and return the figure.
    Optionally saves the figure if 'out_path' is given.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    df[column].sort_values(ascending=False).plot(kind="bar", color=color, ax=ax)

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Sector (ETF)")
    plt.tight_layout()

    _maybe_save(fig, out_path)
    return fig 

# Specific plots built using the function that I defined (_bar_plot)
# Bar plot of mean annual returns for each ETF
def plot_sector_mean(summary_df: pd.DataFrame, out_path: str | Path = None):
    return _bar_plot(
        summary_df, "MeanReturn", "Mean Annual Return (ETFs)", "Return", "skyblue", out_path
    )

# Bar plot of annualized volatility for each ETF
def plot_sector_volatility(summary_df: pd.DataFrame, out_path: str | Path = None):
     return _bar_plot(
        summary_df, "Volatility", "Annualized Volatility (ETFs)", "Volatility", "orange", out_path
    )

# Bar plot of Sharpe ratios for each ETF
def plot_sector_sharpe(summary_df: pd.DataFrame, out_path: str | Path = None):
     return _bar_plot(
        summary_df, "Sharpe", "Sharpe Ratio (ETFs)", "Sharpe", "mediumseagreen", out_path
    )

# Heatmap showing pairwise correlations among ETFs
def plot_sector_corr_heatmap(corr_df: pd.DataFrame, out_path: str | Path = None):
    """
    Plot correlation matrix as a heatmap and return the figure.
    """
    fig, ax = plt.subplots(figsize=(5.5, 5))
    sns.heatmap(
        corr_df, annot=True, cmap="coolwarm",
        vmin=-1, vmax=1, square=True, fmt=".2f", ax=ax
    )
    ax.set_title("Correlation Matrix (ETFs)")
    plt.tight_layout()

    _maybe_save(fig, out_path)
    return fig

# Cumulative growth of 1 euro per ETF
# start from 1 then multiply by (1 + daily return)
def plot_cumulative_returns(returns: pd.DataFrame, out_path: str | Path = None):
    """
    Plot cumulative growth of 1€ invested in each ETF and return the figure.
    """
    growth = (1 + returns).cumprod() # turn daily returns into a cumulative growth index
    fig, ax = plt.subplots(figsize=(8,5)) # create the figure
    growth.plot(ax=ax) # plot all ETFs

    ax.set_title("Cumulative Growth of 1€ by Sector ETF")
    ax.set_ylabel("Growth of 1€")
    ax.set_xlabel("Date")
    plt.tight_layout()

    _maybe_save(fig, out_path)
    return fig
