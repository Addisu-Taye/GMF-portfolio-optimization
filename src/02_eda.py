"""
Task Number: Task 1
File Path: src/02_eda.py
Created by: Addisu Taye
Date: August 12, 2025

Purpose:
This module performs comprehensive Exploratory Data Analysis (EDA) on financial time series data for Tesla (TSLA), Vanguard Total Bond Market ETF (BND), and S&P 500 ETF (SPY), supporting the portfolio optimization challenge at Guide Me in Finance (GMF) Investments. The analysis is based on cleaned historical data loaded from 'data/raw/stock_data.pkl'. The primary objectives are to:
- Understand trends, volatility, and return distributions.
- Test for stationarity (critical for ARIMA modeling).
- Calculate foundational risk metrics such as Value at Risk (VaR) and Sharpe Ratio.
- Generate visualizations to support insights for forecasting and portfolio optimization in subsequent tasks.

This script fulfills Task 1 of the challenge: "Preprocess and Explore the Data" by delivering statistical insights, visual analysis, and risk assessment necessary for informed model development.

Features:
- Loads pre-fetched stock price data using pandas.
- Computes daily percentage returns and 30-day rolling volatility for risk analysis.
- Conducts Augmented Dickey-Fuller (ADF) tests to assess stationarity of TSLA prices and returns.
- Calculates key financial risk/return metrics:
    - 95% Value at Risk (VaR) for TSLA.
    - Annualized Sharpe Ratio (assuming risk-free rate ~0% for simplicity).
- Generates and saves professional-grade visualizations:
    - Historical adjusted closing prices (2015–2025).
    - Distribution of daily returns.
- Saves plots to 'assets/figures/' for inclusion in the final Investment Memo.
- Outputs key results to the console for quick review.

Dependencies:
- pandas: For data manipulation.
- numpy: For numerical operations.
- matplotlib & seaborn: For data visualization.
- statsmodels: For ADF stationarity test.
- joblib: Not used in this script (reserved for model persistence in later tasks).

Usage:
Run after executing 01_data_extraction.py to ensure data is available.
    python src/02_eda.py

Output:
- Console logs: ADF test results, VaR, and Sharpe Ratio.
- Saved figures:
    - assets/figures/price_trend.png
    - assets/figures/returns_volatility.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import joblib

# Load data
df = pd.read_pickle("data/raw/stock_data.pkl")

# Calculate daily returns and rolling volatility
returns = df.pct_change().dropna()
volatility = returns.rolling(30).std()  # 30-day rolling standard deviation

# Stationarity Test: Augmented Dickey-Fuller
def adf_test(series, name):
    """
    Perform ADF test and print result with interpretation.
    
    Args:
        series (pd.Series): Time series to test.
        name (str): Name of the series for display.
    """
    result = adfuller(series.dropna())
    print(f"{name} ADF p-value: {result[1]:.4f} -> {'Stationary' if result[1] < 0.05 else 'Non-Stationary'}")

# Run ADF tests
adf_test(df["TSLA"], "TSLA Price")
adf_test(returns["TSLA"], "TSLA Returns")

# Risk Metrics
var_tsla = np.percentile(returns["TSLA"], 5)  # 95% VaR (left tail)
sharpe_tsla = returns["TSLA"].mean() / returns["TSLA"].std() * np.sqrt(252)  # Annualized Sharpe

print(f"95% VaR: {var_tsla:.2%}")
print(f"Sharpe Ratio: {sharpe_tsla:.2f}")

# Visualization
plt.figure(figsize=(12, 6))
df.plot(title="Adjusted Close Prices (2015–2025)", fontsize=12)
plt.ylabel("Price ($)", fontsize=12)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig("assets/figures/price_trend.png", dpi=150)
plt.close()

returns.plot.hist(bins=100, alpha=0.7, title="Distribution of Daily Returns", figsize=(10, 6))
plt.xlabel("Daily Return", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.tight_layout()
plt.savefig("assets/figures/returns_volatility.png", dpi=150)
plt.close()