# 🧭 Methodology: Data-Driven Portfolio Optimization Using Time Series Forecasting

This project follows a structured, five-stage methodology to develop a model-driven investment strategy for **Guide Me in Finance (GMF) Investments**.  
The approach integrates **financial data analysis**, **time series forecasting**, **Modern Portfolio Theory (MPT)**, and **backtesting** to optimize portfolio allocation based on forecasted market trends.

The methodology is designed to:
- Extract and analyze real-world financial data.
- Forecast future prices using both classical and deep learning models.
- Optimize asset allocation using MPT.
- Validate the strategy through historical simulation.

It is fully aligned with the business objective of enhancing portfolio performance while managing risk, leveraging **yfinance** data for **TSLA, BND, and SPY** from **July 1, 2015, to July 31, 2025**.

---

## **1. Data Extraction & Preprocessing (Task 1)**

**Data Source**
- Historical data via **yfinance** Python library (Yahoo Finance).
- Includes:
  - Adjusted Close Prices (dividends & splits)
  - Volume
  - Open, High, Low, Close
- Assets: **TSLA**, **BND**, **SPY**
- Period: `2015-07-01` → `2025-07-31`

**Data Cleaning**
- Missing values → forward-fill
- Data types validated: datetime index, float64 prices
- Outlier detection via **Z-score** & visual inspection

**Exploratory Data Analysis (EDA)**
- Price trend visualization
- Daily returns: \( r_t = \frac{P_t - P_{t-1}}{P_{t-1}} \)
- Rolling volatility (30-day std. dev.)
- Stationarity test: **ADF**
- Risk metrics:
  - Value at Risk (VaR) – 95% confidence
  - Annualized Sharpe Ratio

**🔍 Insight**: TSLA’s price series is non-stationary, but returns are stationary → suitable for ARIMA modeling.

---

## **2. Time Series Forecasting (Task 2)**

### Model 1: **ARIMA**
- Captures linear trends & autocorrelation
- **auto_arima** for (p,d,q)
- Train: 2015–2023 | Test: 2024–2025
- Metrics: MAE, RMSE, MAPE

### Model 2: **LSTM**
- Captures non-linear patterns & long-term dependencies
- **Architecture**:
  - 2× LSTM layers (50 units each)
  - Dropout 20%
  - Dense output
- Input: 60-day scaled sequences (MinMaxScaler)
- Train: 50 epochs, batch size 32

| Model | MAE  | RMSE | MAPE  |
|-------|------|------|-------|
| ARIMA | 7.12 | 9.12 | 6.8%  |
| LSTM  | 5.41 | 6.38 | 4.9%  |

✅ **Conclusion**: LSTM outperformed ARIMA → selected for forecasting.

---

## **3. Future Market Trend Forecasting (Task 3)**

**Horizon**: 6–12 months (252 trading days) → Aug 2025 – Jul 2026  
**Method**: Recursive LSTM predictions (each output fed back as input)  
**Confidence Intervals**:
\[
CI(t) = \hat{P}_t \pm 1.96 \times \sigma \times \sqrt{\frac{252}{t}}
\]
- σ = daily return volatility

**Findings**:
- Trend: Moderate upward (+25% over 12 months)
- Volatility: Wider CI over time → growing uncertainty
- Implication: Use forecasts as inputs, not standalone signals

---

## **4. Portfolio Optimization (Task 4)**

**Expected Returns**:
- TSLA: LSTM forecast (annualized)
- BND & SPY: Historical mean returns

**Risk Modeling**:
- Covariance matrix from historical returns

**Optimization**: **MPT** via PyPortfolioOpt
- Generated **Efficient Frontier**
- Identified:
  - Max Sharpe Portfolio
  - Minimum Volatility Portfolio

**Recommended Portfolio**:
| Asset | Weight   |
|-------|----------|
| TSLA  | 27.15%   |
| BND   | 48.32%   |
| SPY   | 24.53%   |

- Expected Return: **9.80%**
- Annual Volatility: **10.20%**
- Sharpe Ratio (rf=3%): **0.667**

✅ **Justification**: Best balance of growth & risk for GMF.

---

## **5. Strategy Backtesting (Task 5)**

**Period**: Aug 1, 2024 – Jul 31, 2025  
**Benchmark**: 60% SPY / 40% BND (static)  
**Method**:
- Hold optimal weights (no rebalancing)
- Calculate cumulative returns

**Results**:
| Portfolio         | Return  | Sharpe |
|-------------------|---------|--------|
| Optimized Strategy| +14.1%  | 0.712  |
| 60/40 Benchmark   | +10.9%  | 0.410  |

**Conclusion**: Strategy outperformed benchmark in both **absolute** & **risk-adjusted** returns.

---
---

## 📦 Project Structure
gmf-portfolio-optimization/
├── src/ # Core analysis scripts
│ ├── 01_data_extraction.py
│ ├── 02_eda.py
│ ├── 03_forecasting_models.py
│ ├── 04_forecast_future.py
│ ├── 05_portfolio_optimization.py
│ └── 06_backtesting.py
├── backend/ # FastAPI server
├── frontend/ # React dashboard
├── data/raw/ # Raw stock data (saved as .pkl)
├── models/ # Trained models and forecasts
├── assets/figures/ # Generated plots
├── reports/ # Final investment memo
├── generate_final_report.py # DOCX report generator
└── requirements.txt # Python dependencies

yaml
Copy
Edit

---

## 🚀 How to Use This Repository

### 1. Clone the Repository
```bash
git clone https://github.com/Addisu-Taye/GMF-portfolio-optimization.git
cd GMF-portfolio-optimization
2. Set Up the Environment
We recommend using a virtual environment:

bash
Copy
Edit
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Dependencies
bash
Copy
Edit
pip install --upgrade pip
pip install -r requirements.txt
🔹 Requires: yfinance, pandas, numpy, matplotlib, pmdarima, tensorflow, PyPortfolioOpt,  fastapi, uvicorn

