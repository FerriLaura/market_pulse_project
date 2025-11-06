# Market Pulse

**Market Pulse** explores the behavior of different stock market sectors using historical data from Yahoo Finance.
In particular, performance (returns), risk (volatility), risk-adjusted performance (Sharpe ratio) and co-movement between sectors (correlation) were analyzed during the project.


---

## Project's goals

The goals of this project are the following:
- Fetch and clean real stock data using the 'yfinance' API;
- Compute daily returns, annualized mean returns, mean variance, volatility and Sharpe ratio;
- Compare risk-return profile across three different sectors: healthcare, technology and energy; 
- Visualize relationship through correlation heatmaps and summary plots.

**Sectors analyzed**
This project focuses on three major sectors of the U.S. stock market - Technology, Energy and Healthcare - to compare their performance, risk, and interdipendence. 
These sectors were selected because they have different market dynamics and distinct risk-return profile.  

For each sector, I selected three of the largest and most traded companies. 
So each sector was represented by three tickers: 
- Technology was represented by Apple (AAPL), Microsoft (MSFT) and Invidia (NVDA); 
- Energy was represented by Exxon Mobil Corp(XOM), Chevron Corporation (CVX) and ConocoPhilips (COP);
- Healthcare was represented by Johnson & Johnson (JNJ), Pfizer (PFE), AbbVie (ABBV).

All of these are included in major indices as S&P 500 and Dow Jones, they are highly liquid and strongly representatives of their sector's performance. 

## Project structure 
market_pulse_project/
│
├── market_pulse/                # Core source package
│   ├── init.py
│   ├── config.py                # Global constants, sector mapping
│   ├── data.py                  # Data download and storage
│   ├── metrics.py               # Computations (returns, volatility, correlation)
│   └── visualization.py         # Plotting utilities
│
├── main.py                      # Orchestrates the full pipeline
│
├── data/                        # Generated prices
├── outputs/                     # Summary tables & plots
├── requirements.txt
├── README.md
└── .gitignore

The project follows the structure that was just presented. 
- market_pulse/ -> this is the source package, containing all the core Python modules that perform the analysis. 
    - config.py -> stores global constants and configuration variables, such as sector mappings and default parameters for data fetching; 
    - data.py -> handles data collection and storage. It uses the yfinance API to download historical stock prices, clean them and save them as CSV files in the data/ folder. 
    - metrics.py -> contains the mathematical and statisticak comptations. It calculates daily returns, annualized mean, returns, volatility, variance, and correlations, both at the ticker and sector level. The results are saved in the outputs/ folder as CSV files.
    - visualization.py -> generates visual outputs like bar charts (for mean and volatility at the sector level) and heatmaps (for correlations between the three levels analyzed). Also these plots are saved in the outputs/ folder.
- scripts/ -> it's a folder that contains main.py, the orchestration script. 
    - The script integrates all components: it calls the functions from config.py, data.py, metrics.py and visualization.py in sequence to run the full analysis pipeline automatically.
- data/ -> automatically created to store downloaded stock price data in CSV format. 
- outputs/ -> contains the results of the analysis, such as summary tables (.csv) and visualizations (.png).
- requirements.txt -> lists all python dependencies required to reproduce the environment.
- .gitignore -> specifies files and folders (like .venv/ or /data/) that should not be tracked by Git. 
- README.md -> explains the project's goals, structure, methods, and results.

### Branches
In the project, there are two different benaches: 
- main is the early version of the project, in which sectors were characterized by baskets of stocks, equally-weighted. This was the first idea to develop the project, but it is strongly biased. 
- the etf-version is the second branch of the project: the final version. Sectors are directly represented by ETFs, so that there are not problemns linked to weighting of the tickers that compose sectors. 

## Project methods 
This project follows a structured pipeline that transforms raw financial data into quantitative insights about sector preformance, risk and interdipendence. 
Each part of the process - data collection, computation, and visualization - is handled by a dedicated module within the project. 

### 1. Data collection
Historical stock price data were retrieved directly from Yahoo Finance using the yfinance Python library. The data.py script fetches daily adjusted closing prices for each selected ticker over the past year. 
Key parameters are fixed on the config.py module: 
- period: 1 years
- interval: daily
- auto adjust: enabled to account for stock splits and dividends

In data.py script, a function called fetch_prices() is defined to download and organize the price data. 
This function: 
- takes as input a list of tickers (the ones defined in config.py);
- downloads their adjusted closing prices over the selected period;
- cleans missing data;
- saves the resulting table as a CSV file in the data/ folder. 

This creates a structured dataset where: each row corresponds to a trading day; each column corresponds to a company ticker and each value is the adjusted closing price for that day.

### 2. Retutn computation
Once the price data are available, the next step (implemented in metrics.py) is to compute daily returns, which represents the day-to-day percentage change in stock prices. 
The formula is: Rt=(Pt-Pt-1)/Pt-1
This is done automatically in this project using the pandas method .pct_change().
Daily returns are the foundation for all sebsequent financial metrics because they quantify how much one price moves from one day to the next. 


### 3. Performance and risk metrics
Next, the project computes key financial metrics for each sector: 
- mean annual return, which measures expected performance; 
- volatility: which measures risk or uncertainty (standard deviation of returns);
- variance: which represents the spread of returns (square of volatility);
- Sharpe ratio: measures risk-adjusted performance (how much excess return a sector generates per unit of risk).

To annualize the metrics, the script assumes 252 trading days per year (that is the average number of business days in financial markets).

Annualized mean = daily mean * 252
Annualized volatility = daily volatility * radq(252)

The Sharpe ratio is computed as: 
Sharpe Ratio = (mean annual return - Rf)/Volatility
where Rf is the risk-free rate, set to 2%, consistent with typical short-term Treasury yields.

The results are saved in outputs/sector_summary.csv. 

### 4. Correlation analysis 
To explore how sectors move together, the code computes a correlation matrix of sector's returns. This is a way to measure the strenght of the realtionship between sectors: 
- A correlation matrix close to +1 means they move together; 
- A correlation close to 0 means they move independently, 
- A correlation close to -1 means they move in opposite directions. 

Correlation matrix is saved as outputs/sector_corr.csv

The following files can be found in the outputs' folder: 
- summary_stats.csv -> the table represents the values of the mean, the variance and the volatility computed for each ticker selected for the analysis. 
- sector_summary.csv -> in this file we can find mean, variance, volatility and Sharpe ratio computed for each sector analyzed. 
- correlation_matrix.csv -> is the correlation matrix that includes all the tickers analyzed; 
- sector_corr.csv -> is the correlation matrix between the three sectors.

### 5. Visualization
The visualization.py script turns the results into clear and interpretable charts: 
- mean return bar chart (sector_mean.png): compares average performance across sectors; 
- volatility bar chart (sector_volatility.png): shows relative sector risk; 
- Sharpe ratio bar chart (sector_sharpe.png): visualizes which sectors achieved the best risk-adjusted performance;
- Correlation heatmap (sector_corr_heatmap.png): highlights how strongly sectors move together.
All plots are automatically saved as PNG files in the outputs/ folder.

By combining automated data collection, statistical computation and visualization, the project provieds a complete picture of hoe different sectors perform and interact over time.

### 6. Full pipeline
main.py is the orchestration script. It generates the entire workflow from data collection to final visualization.

## Interpretation of results
The analysis of the three sector ETFs — XLK (Technology), XLE (Energy), and XLV (Healthcare) — reveals distinct performance and risk characteristics over the analyzed period. The Technology sector (XLK) shows the strongest results, with an annualized mean return of about 28% and a Sharpe ratio close to 1, indicating excellent risk-adjusted performance. This means that technology stocks have delivered high returns relative to their volatility, efficiently compensating investors for the risk taken.

In contrast, the Energy sector (XLE) exhibits high volatility (~24%) but a slightly negative mean return (−0.5%), leading to a negative Sharpe ratio. This suggests that energy investors faced considerable risk without corresponding returns — likely reflecting the recent instability of oil markets and cyclical price pressures in the energy industry.

The Healthcare sector (XLV) presents the lowest volatility (~17%), confirming its defensive nature, but its mean return (~1.6%) and near-zero Sharpe ratio indicate that it barely outperformed the risk-free benchmark. Healthcare thus behaved as a stable but low-return sector, providing balance rather than growth.

Overall, Technology was the best-performing and most efficient sector, Energy underperformed despite its risk, and Healthcare offered stability with limited upside. These results are consistent with market trends in which growth-oriented sectors have outpaced more cyclical or defensive ones during periods of economic recovery and investor optimism.

All Sharpe ratios in this analysis were computed assuming a 2% annual risk-free rate, which approximates the return on short-term U.S. Treasury bills — a common benchmark in financial analysis. This adjustment ensures that sector performance is measured relative to a virtually riskless investment, helping to determine whether the additional risk taken in each sector is adequately rewarded.

All three sectors show positive but moderate correlations, indicating that they tend to rise and fall together in broad market cycles, but still offer some diversification benefits when combined in a portfolio.
	•	Technology (XLK) and Energy (XLE) share the highest correlation, meaning they are more likely to react similarly to macroeconomic conditions such as GDP growth or inflation expectations.
	•	Healthcare (XLV) remains the most independent sector, with lower correlations to both technology and energy — confirming its traditional role as a defensive, less market-sensitive component in a diversified portfolio.

The correlation structure suggests that while these ETFs are all part of the broader equity market, they respond differently to economic forces. A portfolio combining Technology, Energy, and Healthcare ETFs would therefore benefit from risk reduction through diversification, without sacrificing exposure to both growth and defensive market segments.