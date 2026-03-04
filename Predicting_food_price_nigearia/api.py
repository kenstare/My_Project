from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI(
    title="Nigeria Food Price & Inflation Forecast API",
    description="Predicts price + inflation using real 2002–2023 WFP data",
    version="3.1"
)

# Load models
ARTIFACTS = Path("artifacts")
price_model = joblib.load(ARTIFACTS / "price_model.joblib")
infl_model  = joblib.load(ARTIFACTS / "inflation_model.joblib")
cat_mapping = joblib.load(ARTIFACTS / "cat_mapping.joblib")

class PredictRequest(BaseModel):
    commodity: Optional[str] = None
    market: Optional[str] = None
    country: Optional[str] = "Nigeria"
    province: Optional[str] = None      # admin1 = state
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    price_lag_1: Optional[float] = None        # ← REQUIRED
    price_3m_mean: Optional[float] = None

@app.get("/")
def home():
    return {"message": "API is WORKING! Go to /docs → try POST /predict"}

@app.post("/predict")
def predict(req: PredictRequest):
    # REQUIRED: last month's price
    if req.price_lag_1 is None:
        return {"error": "price_lag_1 (last month's price) is REQUIRED!"}

    # Fill defaults
    data = {
        'commodity': req.commodity or 'Maize (white)',
        'market': req.market or 'Dawanau',
        'admin1': req.province or 'Kano',
        'admin2': 'Unknown',
        'year': req.year or 2025,
        'month': req.month or 12,
        'day': req.day or 15,
        'price_lag_1': req.price_lag_1,
        'price_3m_mean': req.price_3m_mean or req.price_lag_1
    }

    # Encode categories exactly like training
    for col, mapping_list in cat_mapping.items():
        val = str(data.get(col, 'Unknown'))
        data[col] = mapping_list.index(val) if val in mapping_list else 0

    X = pd.DataFrame([data])

    # Predictions
    pred_price = float(price_model.predict(X)[0])
    pred_inflation_pct = float(infl_model.predict(X)[0]) * 100

    return {
        "your_input": req.dict(),
        "forecast": {
            "predicted_price_next_month_ngn": round(pred_price),
            "predicted_monthly_inflation_percent": round(pred_inflation_pct, 2),
            "expected_price_using_inflation_ngn": round(req.price_lag_1 * (1 + pred_inflation_pct/100)),
            "inflation_level": "HIGH (>10%)" if pred_inflation_pct > 10 else
                              "MODERATE (3-10%)" if pred_inflation_pct > 3 else
                              "LOW (0-3%)" if pred_inflation_pct >= 0 else "DEFLATION",
            "data_used": "Real prices only: 2002 → mid-2023"
        }
    }