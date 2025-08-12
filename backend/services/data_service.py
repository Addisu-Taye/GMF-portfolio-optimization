# backend/services/data_service.py
import pandas as pd
import os

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "stock_data.pkl")

def get_historical_prices():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found at {DATA_PATH}")
    df = pd.read_pickle(DATA_PATH)
    return df.reset_index().to_dict('records')

def get_returns():
    df = pd.read_pickle(DATA_PATH)
    returns = df.pct_change().dropna()
    return returns.reset_index().to_dict('records')