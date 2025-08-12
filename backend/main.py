# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.data import router as data_router
from backend.routers.forecast import router as forecast_router
from backend.routers.portfolio import router as portfolio_router

app = FastAPI(title="GMF Portfolio Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Correct: Prefix added here
app.include_router(data_router, prefix="/api/data", tags=["Data"])
app.include_router(forecast_router, prefix="/api/forecast", tags=["Forecast"])
app.include_router(portfolio_router, prefix="/api/portfolio", tags=["Portfolio"])

@app.get("/")
def root():
    return {"message": "GMF Portfolio API is running!"}