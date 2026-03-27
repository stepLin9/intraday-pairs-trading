# Intraday Pairs Trading Strategy

An intraday statistical arbitrage project that explores mean-reversion trading using equity pairs. This repository implements a modular pipeline for pair validation, spread construction, signal generation, and vectorized backtesting using Python.

## Project Overview

Pairs trading is a market-neutral strategy that identifies two historically related assets and trades temporary deviations in their relative pricing. The core idea is that if the price relationship between two assets is stable, short-term dislocations may revert toward equilibrium.

In this project, I built an intraday pairs trading framework that:

- loads and cleans 1-minute equity data
- tests whether a candidate pair is sufficiently related
- constructs a spread using a hedge ratio estimated by OLS
- evaluates mean reversion using stationarity diagnostics and half-life estimation
- generates long/short trading signals from spread z-scores
- backtests the strategy with transaction costs and holding-period diagnostics

The project was designed to demonstrate quantitative research workflow, time-series modeling, and disciplined backtesting.

## Strategy Logic

The strategy follows these steps:

1. **Data Preparation**  
   Load intraday price data for two assets, align timestamps, and restrict trading to selected market hours.

2. **Pair Validation**  
   Evaluate correlation and cointegration to determine whether the pair is a reasonable mean-reversion candidate.

3. **Spread Construction**  
   Estimate the hedge ratio with OLS and define the spread as the residual relationship between the two assets.

4. **Spread Diagnostics**  
   Test the spread for stationarity and estimate mean-reversion half-life.

5. **Signal Generation**  
   Standardize the spread into a rolling z-score and generate:
   - **long spread** positions when z-score is sufficiently negative
   - **short spread** positions when z-score is sufficiently positive
   - **flat** positions when the spread reverts toward the mean

6. **Backtesting**  
   Apply lagged positions to avoid look-ahead bias, include transaction costs, and compute performance statistics.

## Repository Structure

```text
intraday-pairs-trading/
├── data/
│   ├── AAPL.csv
│   ├── MSFT.csv
│   ├── SPY.csv
│   └── QQQ.csv
├── notebooks/
│   └── intraday_pairs_trading_demo.ipynb
├── src/
│   ├── __init__.py
│   ├── data_prep.py
│   ├── pair_selection.py
│   ├── spread_construction.py
│   ├── spread_diagnostics.py
│   ├── trading_signals.py
│   ├── backtest.py
│   └── main.py
├── README.md
├── requirements.txt
└── .gitignore