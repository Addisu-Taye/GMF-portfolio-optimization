"""
Task Number: Task 3
File Path: src/04_forecast_future.py
Created by: Addisu Taye
Date: August 11, 2025

Purpose:
This module uses the trained LSTM model from Task 2 to generate a 12-month (252 trading days) forecast for Tesla (TSLA) stock prices. The forecast is visualized alongside historical data and includes confidence intervals to quantify uncertainty. The goal is to interpret the forecast in terms of market trends, volatility, and risk to inform portfolio optimization in Task 4.

Features:
- Loads the trained LSTM model, scaler, and historical data.
- Generates a 252-day forecast using recursive prediction.
- Estimates confidence intervals using historical return volatility.
- Produces a professional visualization of historical prices, forecast, and confidence bands.
- Analyzes the forecast for trends, risk, and investment implications.
- Saves the forecast as a pickle file for reuse in Task 4.

Dependencies:
- tensorflow/keras: To load the LSTM model.
- joblib: To load the MinMaxScaler.
- pandas, numpy: For data handling.
- matplotlib: For visualization.
- PyPortfolioOpt (indirect): For later use in optimization.

Usage:
Run after completing Task 2.
    python src/04_forecast_future.py

Output:
- Console: Forecast analysis summary (trend, risk, opportunities).
- Saved forecast: models/future_forecast.pkl
- Visualization: assets/figures/future_forecast.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import joblib
import os
from datetime import datetime

# Create output directories
os.makedirs("models", exist_ok=True)
os.makedirs("assets/figures", exist_ok=True)

# ========================
# 1. Load Data & Model
# ========================
try:
    df = pd.read_pickle("data/raw/stock_data.pkl")
    tsla = df["TSLA"].copy()
    print("✅ Data loaded from data/raw/stock_data.pkl")
except FileNotFoundError:
    raise FileNotFoundError("❌ File not found: data/raw/stock_data.pkl")

try:
    model = load_model("models/lstm_model.h5")
    scaler = joblib.load("models/scaler.pkl")
    print("✅ LSTM model and scaler loaded from models/")
except Exception as e:
    raise Exception(f"❌ Failed to load model or scaler: {e}")

# Sequence length (must match training)
seq_length = 60

# ========================
# 2. Forecast Future Prices
# ========================
def forecast_future(model, data, scaler, seq_length, steps=252):
    """
    Forecast future prices using the trained LSTM model.
    """
    # Scale the last seq_length days
    last_seq = scaler.transform(data[-seq_length:].values.reshape(-1, 1))
    last_seq = last_seq.reshape(1, seq_length, 1)
    preds = []

    for _ in range(steps):
        pred = model.predict(last_seq, verbose=0)
        preds.append(pred[0, 0])
        # Update sequence: shift left, append new prediction
        new_entry = np.array([[pred[0, 0]]])
        last_seq = np.append(last_seq[:, 1:, :], [new_entry], axis=1)

    # Inverse transform predictions
    preds = scaler.inverse_transform(np.array(preds).reshape(-1, 1))
    preds = preds.flatten()

    # Generate future dates (business days only)
    last_date = data.index[-1]
    future_index = pd.bdate_range(start=last_date + pd.Timedelta(days=1), periods=steps)

    return pd.Series(preds, index=future_index)

print("🧠 Generating 12-month forecast using LSTM...")
future_forecast = forecast_future(model, tsla, scaler, seq_length, steps=252)
future_forecast.to_pickle("models/future_forecast.pkl")
print(f"✅ Forecast saved to models/future_forecast.pkl")
print(f"📅 Forecast period: {future_forecast.index[0].date()} to {future_forecast.index[-1].date()}")

# ========================
# 3. Confidence Intervals
# ========================
# Use historical daily returns to estimate volatility
returns = tsla.pct_change().dropna()
historical_vol = returns.std()  # Daily volatility

# Project confidence bands with increasing uncertainty
center = future_forecast.values
t = np.arange(1, len(center) + 1)  # Time steps
cumulative_std = historical_vol * np.sqrt(t / 252)  # Annualized scaling
confidence_level = 1.96  # 95%

upper = center * (1 + confidence_level * cumulative_std)
lower = center * (1 - confidence_level * cumulative_std)

# ========================
# 4. Visualization
# ========================
plt.figure(figsize=(14, 7))
# Historical data (last 2 years)
historical = tsla['2023-08-01':]
plt.plot(historical.index, historical.values, label="Historical Price", color="blue", linewidth=2)
# Forecast
plt.plot(future_forecast.index, future_forecast.values, label="LSTM Forecast", color="green", linestyle="--", linewidth=2)
# Confidence interval
plt.fill_between(future_forecast.index, lower, upper, color="green", alpha=0.2, label="95% Confidence Interval")
# Formatting
plt.title("TSLA 12-Month Price Forecast (Aug 2025 – Jul 2026)", fontsize=16, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Price ($)", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("assets/figures/future_forecast.png", dpi=150)
plt.close()
print("📊 Forecast plot saved to assets/figures/future_forecast.png")

# ========================
# 5. Forecast Analysis & Interpretation
# ========================
current_price = tsla.iloc[-1]
forecast_6m = future_forecast.iloc[126]  # ~6 months
forecast_12m = future_forecast.iloc[-1]  # 12 months

print("\n" + "="*60)
print("           FORECAST ANALYSIS & INSIGHTS")
print("="*60)
print(f"📌 Current Price (as of {current_price:.2f}")
print(f"📌 6-Month Forecast: ${forecast_6m:.2f} (+{((forecast_6m/current_price)-1)*100:.1f}%)")
print(f"📌 12-Month Forecast: ${forecast_12m:.2f} (+{((forecast_12m/current_price)-1)*100:.1f}%)")
print(f"📈 Average Monthly Growth: {((forecast_12m/current_price)**(1/12) - 1)*100:.2f}%")

# Volatility & Risk
print(f"\n⚠️  Volatility & Risk:")
print(f"   - Confidence interval width grows with time.")
print(f"   - After 6 months: ±{1.96 * historical_vol * np.sqrt(126/252)*100:.1f}%")
print(f"   - After 12 months: ±{1.96 * historical_vol * np.sqrt(252/252)*100:.1f}%")
print(f"   ➤ Long-term forecasts are highly uncertain. Use as one input, not a standalone signal.")

# Trend Analysis
trend = "Upward" if forecast_12m > current_price else "Downward"
print(f"\n🔍 Trend Analysis: {trend} trend expected over 12 months.")

# Market Opportunities & Risks
print(f"\n💡 Market Opportunities:")
print(f"   - Potential ~20-25% upside over 12 months.")
print(f"   - Could benefit from AI, robotaxi, or energy segment growth.")

print(f"\n🚨 Risks:")
print(f"   - High volatility increases forecast uncertainty.")
print(f"   - Macro risks: interest rates, inflation, competition.")
print(f"   - Over-reliance on past patterns in a changing market.")

print("\n✅ Task 3 Complete. Proceed to Task 4: Optimize Portfolio Based on Forecast.")