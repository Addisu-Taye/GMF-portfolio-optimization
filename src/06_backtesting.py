"""
Task Number: Task 5
File Path: src/06_backtesting.py
Created by: Addisu Taye
Date: August 12, 2025

Purpose:
This module performs a backtest of the optimized portfolio strategy developed in Task 4 against a traditional 60/40 benchmark (SPY/BND). The backtest covers the period from August 1, 2024, to July 31, 2025, simulating a "hold" strategy based on the optimal weights. The goal is to evaluate whether the model-driven approach outperforms a passive benchmark in terms of total return and risk-adjusted performance (Sharpe Ratio). This provides empirical validation for the investment recommendation.

Features:
- Loads historical price data and optimal portfolio weights.
- Defines the backtesting period: 2024-08-01 to 2025-07-31.
- Constructs two portfolios:
    - Strategy: Optimal weights from Task 4 (27% TSLA, 48% BND, 25% SPY).
    - Benchmark: 60% SPY / 40% BND (classic balanced portfolio).
- Simulates daily portfolio returns and cumulative performance.
- Plots cumulative returns of both portfolios.
- Computes and compares:
    - Total return
    - Annualized Sharpe Ratio (risk-free rate = 3%)
- Outputs a conclusion on strategy performance.

Dependencies:
- pandas, numpy: For data handling and return calculation.
- matplotlib: For performance visualization.
- joblib: To load optimal weights.

Usage:
Run after completing Task 4.
    python src/06_backtesting.py

Output:
- Console: Total return and Sharpe ratio for both strategy and benchmark.
- Visualization: assets/figures/backtest_comparison.png
- Conclusion: Did the strategy outperform?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os

# Create output directories
os.makedirs("assets/figures", exist_ok=True)

# ========================
# 1. Load Data
# ========================
try:
    df = pd.read_pickle("data/raw/stock_data.pkl")
    print("✅ Data loaded from data/raw/stock_data.pkl")
except FileNotFoundError:
    raise FileNotFoundError("❌ File not found: data/raw/stock_data.pkl")

try:
    optimal_weights = joblib.load("models/optimal_weights.pkl")
    print("✅ Optimal weights loaded from models/optimal_weights.pkl")
except FileNotFoundError:
    raise FileNotFoundError("❌ File not found: models/optimal_weights.pkl")

# Define backtesting period
backtest_start = "2024-08-01"
backtest_end = "2025-07-31"
backtest_df = df[backtest_start:backtest_end].copy()

# Ensure no missing dates
backtest_df = backtest_df.asfreq('D').ffill()

print(f"📅 Backtesting Period: {backtest_df.index.min().date()} to {backtest_df.index.max().date()}")
print(f"📊 Data points: {len(backtest_df)}")

# ========================
# 2. Define Portfolios
# ========================
# Strategy: Optimal weights from Task 4
weights_strategy = pd.Series(optimal_weights)

# Benchmark: 60% SPY / 40% BND
weights_benchmark = pd.Series({
    "TSLA": 0.0,
    "BND": 0.4,
    "SPY": 0.6
})

# ========================
# 3. Calculate Portfolio Returns
# ========================
# Daily returns of assets
asset_returns = backtest_df.pct_change().dropna()

def portfolio_cumulative_returns(returns_df, weights):
    """
    Compute cumulative returns for a portfolio.
    """
    weighted_returns = (returns_df * weights).sum(axis=1)
    cum_returns = (1 + weighted_returns).cumprod()
    return cum_returns

# Simulate strategy and benchmark
cumulative_strategy = portfolio_cumulative_returns(asset_returns, weights_strategy)
cumulative_benchmark = portfolio_cumulative_returns(asset_returns, weights_benchmark)

# ========================
# 4. Performance Metrics
# ========================
def annualized_sharpe_ratio(returns, rf=0.03):
    """
    Calculate annualized Sharpe ratio.
    """
    excess_returns = returns - rf / 252
    return (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)

sharpe_strategy = annualized_sharpe_ratio(cumulative_strategy.pct_change().dropna())
sharpe_benchmark = annualized_sharpe_ratio(cumulative_benchmark.pct_change().dropna())

total_return_strategy = (cumulative_strategy.iloc[-1] - 1) * 100
total_return_benchmark = (cumulative_benchmark.iloc[-1] - 1) * 100

# ========================
# 5. Visualization
# ========================
plt.figure(figsize=(14, 7))
plt.plot(cumulative_strategy.index, cumulative_strategy.values,
         label=f"Optimized Strategy ({total_return_strategy:.1f}% return)", color="blue", linewidth=2)
plt.plot(cumulative_benchmark.index, cumulative_benchmark.values,
         label=f"60/40 Benchmark ({total_return_benchmark:.1f}% return)", color="red", linestyle="--", linewidth=2)

plt.title("Backtest: Model-Driven Strategy vs 60/40 Benchmark (Aug 2024 – Jul 2025)", fontsize=16, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Cumulative Return", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("assets/figures/backtest_comparison.png", dpi=150)
plt.close()
print("📊 Backtest plot saved to assets/figures/backtest_comparison.png")

# ========================
# 6. Results & Conclusion
# ========================
print("\n" + "="*60)
print("           BACKTESTING RESULTS")
print("="*60)
print(f"{'Portfolio':<15} {'Total Return':<15} {'Sharpe Ratio':<15}")
print("-"*60)
print(f"{'Strategy':<15} {total_return_strategy:<15.1f} {sharpe_strategy:<15.3f}")
print(f"{'Benchmark':<15} {total_return_benchmark:<15.1f} {sharpe_benchmark:<15.3f}")
print("="*60)

# Conclusion
outperformed_return = total_return_strategy > total_return_benchmark
outperformed_sharpe = sharpe_strategy > sharpe_benchmark

print("\n💡 Conclusion:")
if outperformed_return and outperformed_sharpe:
    print("✅ The model-driven strategy **outperformed** the 60/40 benchmark in both total return and risk-adjusted performance.")
    print("This supports the viability of using forecasting and MPT for portfolio optimization.")
elif outperformed_return:
    print("🔶 The strategy achieved higher total return but a lower Sharpe ratio.")
    print("It delivered growth at higher risk.")
else:
    print("⚠️ The benchmark outperformed the strategy.")
    print("The model-driven approach may need refinement (e.g., re-forecasting, better risk modeling).")

print("\n✅ Task 5 Complete. All tasks finished. Proceed to Final Submission.")

# Optional: Save results
results = {
    "strategy_return": total_return_strategy,
    "benchmark_return": total_return_benchmark,
    "strategy_sharpe": sharpe_strategy,
    "benchmark_sharpe": sharpe_benchmark,
    "outperformed": outperformed_return and outperformed_sharpe
}
joblib.dump(results, "models/backtest_results.pkl")