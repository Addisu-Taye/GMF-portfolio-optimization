from fastapi import APIRouter
from backend.services.data_service import get_historical_prices, get_returns

router = APIRouter()  # ← No prefix here

@router.get("/prices")  # ← Only the endpoint, not full path
def read_prices():
    return get_historical_prices()

@router.get("/returns")
def read_returns():
    return get_returns()