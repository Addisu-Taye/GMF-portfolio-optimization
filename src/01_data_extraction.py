import yfinance as yf
import pandas as pd
import joblib

def fetch_data():
    symbols = ["TSLA", "BND", "SPY"]
    data = yf.download(
        symbols,
        start="2015-07-01",
        end="2025-07-31",
        progress=False
    )
    prices = data["Adj Close"].copy()
    volumes = data["Volume"]
    prices.to_pickle("data/raw/stock_data.pkl")
    volumes.to_pickle("data/raw/volume_data.pkl")
    return prices

if __name__ == "__main__":
    df = fetch_data()
    print("Data saved to data/raw/stock_data.pkl")
    