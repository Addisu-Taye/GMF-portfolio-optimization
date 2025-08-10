"""
Task Number: Task 1
File Path: src/01_data_extraction.py
Created by: Addisu Taye
Date: August 12, 2025

Purpose:
This module is part of the Week 11 challenge for 10 Academy - KAIM, designed to support data-driven portfolio optimization at Guide Me in Finance (GMF) Investments. The primary purpose of this script is to extract historical financial data for three key assets — Tesla (TSLA), Vanguard Total Bond Market ETF (BND), and S&P 500 ETF (SPY) — using the `yfinance` API. The data spans from July 1, 2015, to July 31, 2025, and includes adjusted closing prices and trading volumes. This data serves as the foundational input for subsequent tasks including exploratory data analysis (EDA), time series forecasting, portfolio optimization, and backtesting.

Features:
- Utilizes the `yfinance` library to fetch real-time and historical market data.
- Extracts 'Adj Close' (adjusted for splits and dividends) and 'Volume' for accurate financial analysis.
- Saves cleaned and structured data into pickle (.pkl) files under the data/raw/ directory for reproducibility and efficient loading in downstream tasks.
- Ensures data persistence and modularity by separating data extraction from modeling and analysis.
- Includes basic console feedback upon successful execution.

Dependencies:
- yfinance: For downloading stock data.
- pandas: For data manipulation and storage.
- joblib: For serializing data (alternative to pickle; used here for consistency with scikit-learn workflows).

Usage:
Run this script as a standalone module to download and save financial data:
    python src/01_data_extraction.py

Output:
- data/raw/stock_data.pkl: Contains adjusted closing prices for TSLA, BND, and SPY.
- data/raw/volume_data.pkl: Contains daily trading volumes for the three assets.
"""

import yfinance as yf
import pandas as pd
import joblib

def fetch_data():
    """
    Fetches historical financial data for TSLA, BND, and SPY from Yahoo Finance.

    Returns:
        pd.DataFrame: DataFrame containing adjusted closing prices indexed by date.
    """
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