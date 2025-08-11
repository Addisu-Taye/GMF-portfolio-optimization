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
import os

# Ensure output directory exists
os.makedirs("assets/figures", exist_ok=True)

# ========================
# 1. Load Data
# ========================
try:
    df = pd.read_pickle("data/raw/stock_data.pkl")
    print("✅ Data successfully loaded from data/raw/stock_data.pkl")
except FileNotFoundError:
    raise FileNotFoundError("❌ File not found: data/raw/stock_data.pkl. Please run 01_data_extraction.py first.")

# Ensure index is datetime
df.index = pd.to_datetime(df.index)
print(f"📅 Data range: {df.index.min().date()} to {df.index.max().date()}")
print(f"📊 Data shape: {df.shape}")

# ========================
# 2. Basic Statistics
# ========================
print("\n📈 Basic Statistics (Adj Close):")
print(df.describe().round(2))

# ========================
# 3. Daily Returns & Volatility
# ========================
returns = df.pct_change().dropna()
rolling_volatility = returns["TSLA"].rolling(window=30).std()  # 30-day rolling volatility

print(f"\n📉 TSLA Average Daily Return: {returns['TSLA'].mean():.4f}")
print(f"📈 TSLA Std Dev (Daily): {returns['TSLA'].std():.4f}")

# ========================
# 4. Stationarity Test (ADF)
# ========================
def adf_test(series, title):
    """
    Perform Augmented Dickey-Fuller test and print result.
    """
    result = adfuller(series.dropna(), autolag='AIC')
    print(f"\n🔍 ADF Test: {title}")
    print(f"   ADF Statistic: {result[0]:.6f}")
    print(f"   p-value: {result[1]:.6f}")
    print(f"   # Lags: {result[2]}")
    print(f"   Critical Values:")
    for k, v in result[4].items():
        print(f"      {k}: {v:.3f}")
    print(f"   ➤ {'✅ Stationary' if result[1] < 0.05 else '❌ Non-Stationary'}")

# Run ADF tests
adf_test(df["TSLA"], "TSLA Price (Level)")
adf_test(returns["TSLA"], "TSLA Daily Returns")

# ========================
# 5. Risk Metrics
# ========================
# 95% Value at Risk (VaR) - Historical method
var_95_tsla = np.percentile(returns["TSLA"], 5)
var_99_tsla = np.percentile(returns["TSLA"], 1)

# Annualized Sharpe Ratio (assuming risk-free rate ≈ 0 for simplicity)
sharpe_ratio_tsla = (returns["TSLA"].mean() / returns["TSLA"].std()) * np.sqrt(252)

print(f"\n🛡️  Risk Metrics for TSLA:")
print(f"   95% VaR (1-day): {var_95_tsla:.2%}")
print(f"   99% VaR (1-day): {var_99_tsla:.2%}")
print(f"   Annualized Sharpe Ratio: {sharpe_ratio_tsla:.3f}")

# ========================
# 6. Visualizations
# ========================

# 6.1 Adjusted Close Prices Over Time
plt.figure(figsize=(14, 7))
for col in df.columns:
    plt.plot(df.index, df[col], label=col)
plt.title("Adjusted Close Prices (2015–2025)", fontsize=16, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Price ($)", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("assets/figures/price_trend.png", dpi=150)
plt.close()
print("📊 Figure saved: assets/figures/price_trend.png")

# 6.2 Distribution of Daily Returns
plt.figure(figsize=(12, 6))
for col in returns.columns:
    sns.histplot(returns[col], bins=100, kde=True, label=col, alpha=0.6)
plt.title("Distribution of Daily Returns", fontsize=16, fontweight='bold')
plt.xlabel("Daily Return", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("assets/figures/returns_volatility.png", dpi=150)
plt.close()
print("📊 Figure saved: assets/figures/returns_volatility.png")

# 6.3 Rolling Volatility (Optional extra plot)
plt.figure(figsize=(12, 6))
plt.plot(returns.index, rolling_volatility, label="TSLA 30-Day Rolling Volatility", color='red')
plt.title("30-Day Rolling Volatility of TSLA", fontsize=16, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Volatility (Std Dev)", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("assets/figures/rolling_volatility.png", dpi=150)
plt.close()
print("📊 Figure saved: assets/figures/rolling_volatility.png")

# ========================
# 7. Outlier Detection
# ========================
extreme_returns = returns[returns.abs() > 0.08]  # Threshold: 8% daily move
if not extreme_returns.empty:
    print(f"\n🚨 Detected {len(extreme_returns)} extreme daily returns (>8%):")
    print(extreme_returns.round(4))
else:
    print("\n✅ No extreme daily returns (>8%) detected.")

# ========================
# 8. Correlation Analysis
# ========================
correlation = returns.corr()
print(f"\n🔗 Correlation Matrix (Daily Returns):")
print(correlation.round(4))

# Plot correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, square=True)
plt.title("Correlation Matrix of Daily Returns", fontsize=14)
plt.tight_layout()
plt.savefig("assets/figures/correlation_heatmap.png", dpi=150)
plt.close()
print("📊 Figure saved: assets/figures/correlation_heatmap.png")

print("\n✅ EDA Complete. Proceed to Task 2: Time Series Forecasting.")