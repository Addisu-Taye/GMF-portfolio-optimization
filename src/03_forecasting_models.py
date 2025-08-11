"""
Task Number: Task 2
File Path: src/03_forecasting_models.py
Created by: Addisu Taye
Date: August 11, 2025

Purpose:
This module implements and compares two time series forecasting models—ARIMA and LSTM—to predict Tesla (TSLA) stock prices. The goal is to evaluate model performance and select the best approach for forecasting future prices, which will inform portfolio optimization in subsequent tasks. This task fulfills the requirement to use both a classical statistical model (ARIMA) and a deep learning model (LSTM) on real financial data with a chronological train-test split.

Features:
- Loads cleaned TSLA price data from 'data/raw/stock_data.pkl'.
- Splits data chronologically: training (2015–2023), testing (2024–2025).
- Implements ARIMA model using `auto_arima` for optimal (p,d,q) selection.
- Implements LSTM model using Keras with 60-day sequence input.
- Evaluates both models using MAE, RMSE, and MAPE.
- Generates and saves a comparative plot of forecasts vs actual test data.
- Outputs performance metrics to console for model comparison.
- Saves trained models and forecasts for reuse in Task 3.

Dependencies:
- pandas, numpy: Data handling.
- yfinance (indirect): Data source (via Task 1).
- pmdarima: For ARIMA modeling and parameter optimization.
- tensorflow/keras: For LSTM model.
- sklearn: For evaluation metrics.
- matplotlib: For visualization.
- joblib: For model and forecast persistence.

Usage:
Run after completing Task 1 (data extraction and EDA).
    python src/03_forecasting_models.py

Output:
- Console: Model performance metrics (MAE, RMSE, MAPE).
- Saved models:
    - models/arima_model.pkl
    - models/lstm_model.h5
    - models/scaler.pkl
- Saved forecasts:
    - models/arima_forecast.pkl
    - models/lstm_forecast.pkl
- Visualization:
    - assets/figures/arima_vs_lstm.png
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib
import os

# Create required directories
os.makedirs("models", exist_ok=True)
os.makedirs("assets/figures", exist_ok=True)

# ========================
# 1. Load Data
# ========================
try:
    df = pd.read_pickle("data/raw/stock_data.pkl")
    tsla = df["TSLA"].copy()
    print("✅ Data loaded successfully from data/raw/stock_data.pkl")
except FileNotFoundError:
    raise FileNotFoundError("❌ File not found: data/raw/stock_data.pkl. Please run Task 1 first.")

# ========================
# 2. Chronological Train-Test Split
# ========================
# Train: 2015–2023 | Test: 2024–2025
train = tsla[:'2023-12-31']
test = tsla['2024-01-01':]

print(f"📊 Training period: {train.index.min().date()} to {train.index.max().date()} ({len(train)} days)")
print(f"📈 Testing period: {test.index.min().date()} to {test.index.max().date()} ({len(test)} days)")

# Ensure test index alignment
test_index = test.index

# ========================
# 3. ARIMA Model
# ========================
print("\n🔍 Fitting ARIMA Model...")
arima_model = auto_arima(
    train,
    seasonal=False,
    trace=True,
    error_action='ignore',
    suppress_warnings=True,
    stepwise=True,
    n_fits=10
)

# Forecast
forecast_arima = arima_model.predict(n_periods=len(test))
forecast_arima_series = pd.Series(forecast_arima, index=test_index)

# Save
joblib.dump(arima_model, "models/arima_model.pkl")
forecast_arima_series.to_pickle("models/arima_forecast.pkl")

# Metrics
mae_arima = mean_absolute_error(test, forecast_arima)
rmse_arima = np.sqrt(mean_squared_error(test, forecast_arima))
mape_arima = mean_absolute_percentage_error(test, forecast_arima) * 100

print(f"ARIMA - MAE: {mae_arima:.2f}, RMSE: {rmse_arima:.2f}, MAPE: {mape_arima:.2f}%")

# ========================
# 4. LSTM Model
# ========================
print("\n🧠 Building and Training LSTM Model...")

# Scale data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_train = scaler.fit_transform(train.values.reshape(-1, 1))
scaled_test = scaler.transform(test.values.reshape(-1, 1))

# Create sequences (60-day window)
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

seq_length = 60
X_train, y_train = create_sequences(scaled_train, seq_length)
X_test, y_test = create_sequences(scaled_test, seq_length)

# Build LSTM
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(seq_length, 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, batch_size=32, epochs=50, verbose=0)

# Predict
lstm_pred_scaled = model.predict(X_test, verbose=0)
lstm_pred = scaler.inverse_transform(lstm_pred_scaled)

# Align with test index
lstm_forecast = pd.Series(lstm_pred.flatten(), index=test_index[:len(lstm_pred)])

# Save
model.save("models/lstm_model.h5")
joblib.dump(scaler, "models/scaler.pkl")
lstm_forecast.to_pickle("models/lstm_forecast.pkl")

# Metrics
mae_lstm = mean_absolute_error(test[:len(lstm_pred)], lstm_pred)
rmse_lstm = np.sqrt(mean_squared_error(test[:len(lstm_pred)], lstm_pred))
mape_lstm = mean_absolute_percentage_error(test[:len(lstm_pred)], lstm_pred) * 100

print(f"LSTM   - MAE: {mae_lstm:.2f}, RMSE: {rmse_lstm:.2f}, MAPE: {mape_lstm:.2f}%")

# ========================
# 5. Model Comparison Plot
# ========================
plt.figure(figsize=(14, 7))
plt.plot(train[-200:], label="Training Data", color="blue", alpha=0.7)
plt.plot(test, label="Actual Price", color="black", linewidth=2)
plt.plot(forecast_arima_series, label="ARIMA Forecast", color="red", linestyle="--", alpha=0.8)
plt.plot(lstm_forecast, label="LSTM Forecast", color="green", linewidth=2)

plt.title("ARIMA vs LSTM Forecast vs Actual (TSLA - 2024–2025)", fontsize=16, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Price ($)", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("assets/figures/arima_vs_lstm.png", dpi=150)
plt.close()

print("📊 Forecast comparison plot saved to assets/figures/arima_vs_lstm.png")

# ========================
# 6. Summary & Recommendation
# ========================
print("\n" + "="*60)
print("           MODEL PERFORMANCE COMPARISON")
print("="*60)
print(f"{'Model':<10} {'MAE':<10} {'RMSE':<10} {'MAPE (%)':<10}")
print("-"*60)
print(f"{'ARIMA':<10} {mae_arima:<10.2f} {rmse_arima:<10.2f} {mape_arima:<10.2f}")
print(f"{'LSTM':<10} {mae_lstm:<10.2f} {rmse_lstm:<10.2f} {mape_lstm:<10.2f}")
print("="*60)

if rmse_lstm < rmse_arima:
    print("✅ LSTM outperformed ARIMA based on RMSE.")
    print("💡 Recommendation: Use LSTM for Task 3 forecasting.")
else:
    print("✅ ARIMA outperformed LSTM based on RMSE.")
    print("💡 Recommendation: Use ARIMA for Task 3 forecasting.")

print("✅ Task 2 Complete. Proceed to Task 3: Forecast Future Market Trends.")