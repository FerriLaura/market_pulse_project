# Market Pulse

**Market Pulse** explores the behavior of different stock market sectors using historical data from Yahoo Finance.
It analyzes sector performance, volatility, and correlations to uncover how various parts of the market move together.

---

## Project overview

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

