from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import zipfile
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from scipy.optimize import curve_fit

app = FastAPI(
    title="World Population Forecast API",
    description="Accurate global population forecast 1960–2100 using my data",
    version="3.0"
)

# LOAD DATA & TRAIN MODELS ONCE
print("Loading data and training models...")

zip_path = r"C:\Users\akind\Downloads\Global Population (1).zip"
df = pd.read_csv(zipfile.ZipFile(zip_path).open('Global_annual_population.csv'))
df = df.rename(columns=lambda x: x.strip().replace(',', ''))
df['Year'] = df['Year'].astype(int)
df['Population'] = df['Population'].astype(float)
df['t'] = df['Year'] - 1960

# Cubic model (short-term king)
cubic_model = make_pipeline(PolynomialFeatures(3), Ridge(alpha=1e-10))
cubic_model.fit(df[['Year']], df['Population'])

# Logistic model (long-term king)
def logistic(t, K, r, t0):
    return K / (1 + np.exp(-r * (t - t0)))

popt, _ = curve_fit(
    logistic, df['t'], df['Population'],
    p0=[11.5, 0.029, 52],
    bounds=([9, 0.02, 40], [15, 0.04, 80]),
    maxfev=20000
)
K, r, t0 = popt

print(f"Models ready! Logistic carrying capacity = {K:.3f} billion")

# PREDICTION FUNCTION 
def predict(year: int) -> float:
    if not (1960 <= year <= 2100):
        raise HTTPException(status_code=400, detail="Year must be 1960–2100")
    
    t = year - 1960
    cubic = float(cubic_model.predict(pd.DataFrame({'Year': [year]}))[0])
    logis = logistic(t, *popt)
    
    # Blend: cubic until 2055 → logistic after
    if year <= 2055:
        return round(cubic, 3)
    else:
        weight = min((year - 2055) / 20, 1.0)   # smooth 20-year transition
        return round(cubic * (1 - weight) + logis * weight, 3)

# RESPONSE MODELS
class PredictionResponse(BaseModel):
    year: int
    population_billions: float
    model_used: str
    note: str = ""   # ← now always a string (empty if no note)

# ENDPOINTS 
@app.get("/")
def home():
    return {"message": "World Population API is LIVE!", "docs": "/docs"}

@app.get("/predict/{year}", response_model=PredictionResponse)
def get_prediction(year: int):
    pop = predict(year)
    model = "Cubic Polynomial" if year <= 2055 else "Blended (Cubic → Logistic)"
    note = "Approaching global peak" if year >= 2080 else ""
    
    return PredictionResponse(
        year=year,
        population_billions=pop,
        model_used=model,
        note=note
    )

@app.get("/forecast/{start}/{end}")
def forecast(start: int, end: int):
    if start > end or start < 1960 or end > 2100:
        raise HTTPException(status_code=400, detail="Invalid range")
    return [{"year": y, "population_billions": predict(y)} for y in range(start, end + 1)]

@app.get("/peak")
def peak():
    peak_year = int(1960 + t0 + np.log(K / df.iloc[-1]['Population'] - 1) / r)
    return {
        "estimated_peak_year": peak_year,
        "peak_population_billions": round(K, 3),
        "carrying_capacity_billions": round(K, 3)
    }