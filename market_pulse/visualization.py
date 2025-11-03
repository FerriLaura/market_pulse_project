import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

# Mean return per sector
def plot_sector_mean(summary_df: pd.DataFrame, out_path: str | Path = None):
    plt.figure(figsize=(8, 5))
    summary_df["MeanReturn"].sort_values(ascending=False).plot(kind="bar", color="skyblue")
    plt.title("Mean Annual Return per Sector")
    plt.ylabel("Mean Return")
    plt.xlabel("Sector")
    plt.tight_layout()

    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path)
        print(f"Saved mean return plot to {out_path}")
    else:
        plt.show()

    plt.close()

# Volatility per sector
def plot_sector_volatility(summary_df: pd.DataFrame, out_path: str | Path = None):
    plt.figure(figsize=(8, 5))
    summary_df["Volatility"].sort_values(ascending=False).plot(kind="bar", color="orange")
    plt.title("Volatility per Sector")
    plt.ylabel("Volatility (Annualized)")
    plt.xlabel("Sector")
    plt.tight_layout()

    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path)
        print(f"Saved volatility plot to {out_path}")
    else:
        plt.show()

    plt.close()

# Correlation between sectors
def plot_sector_corr_heatmap(corr_df: pd.DataFrame, out_path: str | Path = None):
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr_df, annot=True, cmap="coolwarm", fmt=".2f", square=True)
    plt.title("Correlation Between Sectors")
    plt.tight_layout()

    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path)
        print(f"Saved correlation heatmap to {out_path}")
    else:
        plt.show()

    plt.close()

# Sharpe per sector
def plot_sector_sharpe(summary_df: pd.DataFrame, out_path: str | Path = None):
    sharpe = summary_df["Sharpe"].sort_values(ascending=False)

    plt.figure(figsize=(8,5))
    ax = sharpe.plot(kind="bar")
    ax.set_title("Sharpe Ratio per Sector")
    ax.set_ylabel("Sharpe (annual)")
    ax.set_xlabel("Sector")
    
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}",
                    (p.get_x() + p.get_width()/2, p.get_height()),
                    ha="center", va="bottom", fontsize=9, rotation=0)

    plt.tight_layout()
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path)
        print(f"Saved Sharpe plot to {out_path}")
    else:
        plt.show()
    plt.close()

if __name__ == "__main__":
    df = pd.read_csv("outputs/sector_summary.csv", index_col=0)
    corr = pd.read_csv("outputs/sector_corr.csv", index_col=0)

    plot_sector_mean(df, "outputs/sector_mean.png")
    plot_sector_volatility(df, "outputs/sector_volatility.png")
    plot_sector_corr_heatmap(corr, "outputs/sector_corr_heatmap.png")