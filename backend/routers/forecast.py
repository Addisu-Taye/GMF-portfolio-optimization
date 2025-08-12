from fastapi import APIRouter
from backend.services.forecast_service import get_forecast, get_model_comparison

router = APIRouter()

@router.get("/future")
def read_forecast():
    return get_forecast()

@router.get("/comparison")
def read_comparison():
    return get_model_comparison()