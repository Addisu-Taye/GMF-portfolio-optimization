from fastapi import APIRouter
from backend.services.portfolio_service import get_optimal_portfolio, get_backtest_results

router = APIRouter()

@router.get("/optimal")
def read_optimal():
    return get_optimal_portfolio()

@router.get("/backtest")
def read_backtest():
    return get_backtest_results()