# Market Pulse

**Market Pulse** explores the behavior of different stock market sectors using historical data from Yahoo Finance.
It analyzes sector performance, volatility, and correlations to uncover how various parts of the market move together.

---

## Project's goals

The goal of this project is to: 
- Fetch and clean real stock data using the 'yfinance' API;
- Compute daily returns, annualized mean returns, mean variance and volatility;
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
├── scripts/
│   └── main.py                  # Orchestrates the full pipeline
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

## Project methods 
This project follows a structured pipeline that transforms raw financial data into quantitative insights about sector preformance, risk and interdipendence. 
Each part of the process - data collection, computation, and visualization - is handled by a dedicated module within the project. 

### 1. Data collection
Historical stock price data were retrieved directly from Yahoo Finance using the yfinance Python library. The data.py script fetches daily adjusted closing prices for each selected ticker over the past year. 
Key parameters are fixed on the config.py module: 
- period: 1 year
- interval: daily
- auto adjust: enabled to account for stock splits and dividends

Each sector is represented by three of the most capitalized companies in the U.S. market.

In data.py script, a function called fetch_prices() is defined to download and organize the price data. 
This function: 
- takes as inputa a list of tickers (the ones defined in config.py);
- downloads their adjusted closing prices over the selected period;
- cleans missing data;
- saves the resulting table as a CSV file in the data/ folder. 

This creates a structured dataset where: each row corresponds to a trading day; each column corresponds to a company ticker and each value is the adjusted closing price for that day.

### 2. Retutn computation
Once the price data are available, the next step (implemented in metrics.py) is to compute daily returns, which represents the day-to-day percentage change in stock prices. 
The formula is: Rt=(Pt-Pt-1)/Pt-1
This is done automatically in this project using the pandas method .pct_change().
Daily returns are the foundation for all sebsequent financial metrics because they quantify how much one price moves from one day to the next. 

### 3. Sector-level aggregation
After computing returns for each ticker, the analysis aggregates them into sector-level daily returns to observe how entire sectors behave. 
This is done in the script main.py using the function make_sector_returns(), which averages the daily returns of all companies within each sector. 
The formula is: R_{\text{sector},t} = \frac{1}{n} \sum_{i=1}^{n} R_{i,t}
This approach gives each company equal weight in its sector, ensuring that one large firm does not domnate the sector's performance. 
The result is a dataset where each column represent one sector (technology, energy and healthcare) and each row shows that sector's average daily return. 

### 4. Performance and risk metrics
Next, the project computes key financial metrics for each sector: 
- mean annual return, which measures expected performance; 
- volatility: which measures risk or uncertainty (standard deviation of returns);
- variance: which represents the spread of returns (square of volatility).

To annualize these three metrics, the script assumes 252 trading days per year (that is the average number of business days in financial markets).

Annualized mean = daily mean * 252
Annualized volatility = daily volatility * radq(252)

The results are saved in outputs/sector_summary.csv

### 5. Correlation analysis 
To explore how sectors move together, the code computes a correlation matrix of sector's returns. This is a way to measure the strenght of the realtionship between sectors: 
- A correlation matrix close to +1 means they move together; 
- A correlation close to 0 means they move independently, 
- A correlation close to -1 means they move in opposite directions. 

Correlation matrix is saved as outputs/sector_corr.csv

### 6. Visualization
The visualization.py script turns the results into clear and interpretable charts: 
- a bar chart for mean returns compares sector performances; 
- a bar chart of volatilities compares sector risk levels; 
- a heatmap of correlations visualizes how sectors move together. 
All plots are automatically saved as PNG files in the outputs/ folder.

By combining automated data collection, statistical computation and visualization, the project provieds a complete picture of hoe different sectors perform and interact over time.

## Conclusions
the analysis compared three major U.S. stock market sectors: Technology, Energy and healthcare, over the past year, using three representatives companies from each.

### Analysis of the sector performance

The **Technology** sector (represented by Apple, Microsoft and NVIDIA) showed the highest mean annual return among the three sectors. This confirms that technology stocks have been the main drivers of market growth in recent years, propelled by innovation in AI, software, and semiconductures. However, such strong returns come with higher exposure to investor sentiment and macroeconomic changes, which can amplify price movements. 

The **Energy sector** (Exxon Mobil, Chevron, and ConocoPhillips) showed moderate but consistent returns.
Its performance is closely tied to global oil demand, production levels, and geopolitical factors.
During periods of high commodity prices, energy stocks tend to outperform the broader market, but they can also experience sharp downturns when oil prices fall.

The **Healthcare sector** (Johnson & Johnson, Pfizer, and AbbVie) recorded the lowest average return, though still positive.
This is coherent with the sector’s historical behavior: healthcare companies offer stable growth due to steady demand for medical products and pharmaceuticals, but they do not experience explosive gains like technology firms.
Their defensive nature makes them a refuge during market uncertainty or downturns. 

### Risk analysis - volatility and variance

The results showed clear differences between sectors: 
- Technology had the highest volatility, confirming that each stocks carry greater risk. Their prices are influenced by innovation cycles, earnings surprises, and investor speculation. 
- Energy exhibited medium-to-high volatility, largely driven by external macroeconomic and geopolitical factors (e.g., oil prices, OPEC decisions, global conflicts).
- Healthcare had the lowest volatility, demonstrating strong price stability and resilience even in volatile market environments.

In financial terms, high volatility means greater uncertainty — while it can lead to higher returns, it also implies higher potential losses.
Thus, investors seeking growth might favor Technology, while those prioritizing stability would lean toward Healthcare.

### Correlation Analysis - sector interdependence

The correlation heatmap provided key insights into how sectors move relative to one another:
- Technology and Healthcare exhibited a low correlation, meaning their price movements are largely independent. This makes them complementary in a diversified portfolio.
- Technology and Energy showed a moderate positive correlation, suggesting that both sectors may respond similarly to broad market trends such as global economic expansion or contraction.
- Energy and Healthcare displayed the weakest correlation, confirming their distinct economic drivers — one driven by commodities, the other by demographic and healthcare needs.

These results support the principle of sector diversification: combining uncorrelated sectors helps reduce portfolio risk without sacrificing overall return potential.
This confirms a classic trade-off in finance: higher expected return usually comes with higher risk.
By mixing these three sectors, an investor can achieve a balanced portfolio that captures growth opportunities while maintaining stability.

While this analysis provides valuable insights, several limitations exist: 
- Only one year of data was used: extending the period would make results more robust; 
- The sectors were represented by three eqaully weighted companies: weighting them by market capitalization could better reflect real-world portfolios;
- The analysis was based on daily data; using rolling windows (e.g. 30-day or 90-day volatility) could reveal how risk evolves over time; 
- Future work could incorporate risk-adjusted performance metrics like Sharpe ratio, or explore sector ETFs instead of individual stocks for broader coverage.

## Interpretation of the plots????