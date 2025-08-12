# backend/services/forecast_service.py
"""
Service layer for handling forecast-related data retrieval.
Uses absolute paths to ensure reliability regardless of execution context.
"""

import joblib
import pandas as pd
import os

# Define BASE_DIR to make paths absolute
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

def get_forecast():
    """
    Load the 12-month TSLA price forecast.
    Returns: List of dicts: [{"date": "YYYY-MM-DD", "price": float}]
    """
    forecast_path = os.path.join(MODELS_DIR, "future_forecast.pkl")
    
    if not os.path.exists(forecast_path):
        raise FileNotFoundError(f"Forecast file not found at {forecast_path}")
    
    try:
        forecast = joblib.load(forecast_path)
        # Ensure it's a Series with datetime index
        if isinstance(forecast, pd.Series):
            return [{"date": str(date), "price": float(price)} for date, price in forecast.items()]
        else:
            raise ValueError("Forecast must be a pandas Series.")
    except Exception as e:
        raise RuntimeError(f"Failed to load forecast: {str(e)}")


def get_model_comparison():
    """
    Load performance metrics for ARIMA and LSTM models.
    Returns: Dict with model names and metrics (RMSE, MAPE).
    """
    metrics_path = os.path.join(MODELS_DIR, "model_comparison.pkl")
    
    # Try to load real metrics if available
    if os.path.exists(metrics_path):
        try:
            metrics = joblib.load(metrics_path)
            return {
                "models": [
                    {"name": "ARIMA", "RMSE": round(metrics["arima_rmse"], 2), "MAPE": round(metrics["arima_mape"], 2)},
                    {"name": "LSTM", "RMSE": round(metrics["lstm_rmse"], 2), "MAPE": round(metrics["lstm_mape"], 2)}
                ]
            }
        except Exception as e:
            print(f"Warning: Failed to load model metrics: {e}")

    # Fallback: Use hardcoded values (from your current code)
    print("Using fallback model comparison metrics.")
    return {
        "models": [
            {"name": "ARIMA", "RMSE": 9.12, "MAPE": 6.8},
            {"name": "LSTM", "RMSE": 6.38, "MAPE": 4.9}
        ]
    }