import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import joblib

df = pd.read_pickle("data/raw/stock_data.pkl")

# Returns
returns = df.pct_change().dropna()
volatility = returns.rolling(30).std()

# ADF Test
def adf_test(series, name):
    result = adfuller(series.dropna())
    print(f"{name} ADF p-value: {result[1]:.4f} -> {'Stationary' if result[1] < 0.05 else 'Non-Stationary'}")

adf_test(df["TSLA"], "TSLA Price")
adf_test(returns["TSLA"], "TSLA Returns")

# VaR and Sharpe
var_tsla = np.percentile(returns["TSLA"], 5)
sharpe_tsla = returns["TSLA"].mean() / returns["TSLA"].std() * np.sqrt(252)

print(f"95% VaR: {var_tsla:.2%}")
print(f"Sharpe Ratio: {sharpe_tsla:.2f}")

# Plotting
plt.figure(figsize=(12, 6))
df.plot(title="Adjusted Close Prices (2015–2025)")
plt.ylabel("Price ($)")
plt.savefig("assets/figures/price_trend.png")
plt.close()

returns.plot.hist(bins=100, alpha=0.7, title="Daily Returns Distribution")
plt.savefig("assets/figures/returns_volatility.png")
plt.close()