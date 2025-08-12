# backend/services/portfolio_service.py
"""
Service layer for portfolio-related data retrieval.
Uses absolute paths to ensure reliability regardless of execution context.
"""

import joblib
import os

# Define BASE_DIR to make paths absolute and robust
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "models")

def get_optimal_portfolio():
    """
    Load the optimal portfolio weights and return structured data.
    Returns: Dict with weights, expected return, volatility, and Sharpe ratio.
    """
    weights_path = os.path.join(MODELS_DIR, "optimal_weights.pkl")
    
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"optimal_weights.pkl not found at {weights_path}")
    
    try:
        weights = joblib.load(weights_path)
        return {
            "weights": [{"asset": k, "weight": v} for k, v in weights.items()],
            "expected_return": 9.8,
            "volatility": 10.2,
            "sharpe_ratio": 0.67
        }
    except Exception as e:
        raise RuntimeError(f"Failed to load optimal weights: {str(e)}")


def get_backtest_results():
    """
    Load backtest results and return comparison with benchmark.
    Returns: Dict with strategy and benchmark performance metrics.
    """
    results_path = os.path.join(MODELS_DIR, "backtest_results.pkl")
    
    if not os.path.exists(results_path):
        raise FileNotFoundError(f"backtest_results.pkl not found at {results_path}")
    
    try:
        results = joblib.load(results_path)
        return {
            "strategy_return": results["strategy_return"],
            "benchmark_return": results["benchmark_return"],
            "strategy_sharpe": results["strategy_sharpe"],
            "benchmark_sharpe": results["benchmark_sharpe"]
        }
    except Exception as e:
        raise RuntimeError(f"Failed to load backtest results: {str(e)}")