import os
# Silence noisy logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"          # no oneDNN messages
os.environ["LOKY_MAX_CPU_COUNT"] = "4"             # no joblib CPU warning

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="joblib")

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from pathlib import Path
import uvicorn
from datetime import datetime
import json
import h5py

app = FastAPI(
    title="Indian Credit Card Intelligence API",
    description="Fraud Detection • High-Spender Prediction • CLV • Churn • Credit Limit",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Minimal debug (only once at startup)
print("Starting API - current dir:", Path.cwd().resolve())

# ────────────────────────────────────────────────
# Custom function to load keras model and remove quantization_config
# ────────────────────────────────────────────────
def load_keras_model_safe(model_path):
    """Load Keras model and handle quantization_config compatibility"""
    try:
        return tf.keras.models.load_model(model_path)
    except TypeError as e:
        if "quantization_config" in str(e):
            # Load the .keras file (which is a ZIP archive with JSON config)
            import tempfile
            import zipfile
            
            with tempfile.TemporaryDirectory() as tmpdir:
                with zipfile.ZipFile(model_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdir)
                
                # Read and fix the config.json
                config_file = Path(tmpdir) / "config.json"
                if config_file.exists():
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    
                    # Remove quantization_config from all Dense layers
                    def remove_quantization(obj):
                        if isinstance(obj, dict):
                            if 'config' in obj and isinstance(obj['config'], dict):
                                obj['config'].pop('quantization_config', None)
                            for v in obj.values():
                                remove_quantization(v)
                        elif isinstance(obj, list):
                            for item in obj:
                                remove_quantization(item)
                    
                    remove_quantization(config)
                    
                    with open(config_file, 'w') as f:
                        json.dump(config, f)
                
                # Repackage and load
                fixed_model_path = Path(tmpdir) / "model_fixed.keras"
                with zipfile.ZipFile(fixed_model_path, 'w') as zip_ref:
                    for file in Path(tmpdir).glob("*"):
                        if file.is_file() and file.name != "model_fixed.keras":
                            zip_ref.write(file, arcname=file.name)
                
                return tf.keras.models.load_model(fixed_model_path)
        else:
            raise

# ────────────────────────────────────────────────
# Load models + optional processed transaction data
# ────────────────────────────────────────────────
MODEL_DIR = Path("models")
df = None

try:
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    le_city = joblib.load(MODEL_DIR / "le_city.pkl")
    le_card = joblib.load(MODEL_DIR / "le_card.pkl")
    le_exp = joblib.load(MODEL_DIR / "le_exp.pkl")
    autoencoder = load_keras_model_safe(MODEL_DIR / "autoencoder.keras")
    high_spender_model = joblib.load(MODEL_DIR / "high_spender_model.pkl")
    fraud_threshold = joblib.load(MODEL_DIR / "fraud_threshold.pkl")

    print("All models loaded.")

    # Try loading PROCESSED data (with Customer_ID, AE_Fraud, etc.)
    try:
        df = pd.read_csv("processed_transactions.csv")
        print("Processed data loaded → /customer/{id}/profile enabled.")
    except FileNotFoundError:
        print("Warning: processed_transactions.csv not found → customer profile disabled.")
    except Exception as e:
        print(f"Processed data load failed: {e}")

except Exception as e:
    raise RuntimeError(f"Failed to load models: {str(e)}\nCheck /models folder.")

# ────────────────────────────────────────────────
# Input model (Pydantic v2 style - no deprecation warnings)
# ────────────────────────────────────────────────
class Transaction(BaseModel):
    Date: str = Field(..., description="DD-MMM-YY e.g. 15-Aug-24")
    City: str
    Card_Type: str = Field(..., alias="Card Type")
    Exp_Type: str = Field(..., alias="Exp Type")
    Gender: str = Field(..., pattern="^[MF]$")
    Amount: float = Field(..., gt=0)

    @field_validator('Date')
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            pd.to_datetime(v, format='%d-%b-%y')
        except Exception:
            raise ValueError("Invalid date. Use DD-MMM-YY e.g. 15-Aug-24")
        return v

    model_config = {"populate_by_name": True}

# ────────────────────────────────────────────────
# Endpoints
# ────────────────────────────────────────────────
@app.get("/")
def home():
    return {"message": "Indian Credit Card Intelligence API – see /docs"}

@app.get("/health")
def health():
    return {"status": "healthy", "models_loaded": True}

@app.post("/predict/fraud")
def predict_fraud(txn: Transaction):
    try:
        city_code = int(le_city.transform([txn.City])[0])
        card_code = int(le_card.transform([txn.Card_Type])[0])
        exp_code = int(le_exp.transform([txn.Exp_Type])[0])
        date = pd.to_datetime(txn.Date, format='%d-%b-%y')

        row = np.array([[txn.Amount, date.month, date.day,
                         1 if date.dayofweek >= 5 else 0,
                         city_code, card_code, exp_code]])

        scaled = scaler.transform(row)
        recon = autoencoder.predict(scaled, verbose=0)
        error = float(np.mean(np.power(scaled - recon, 2)))

        return {
            "is_suspicious": bool(error > fraud_threshold),
            "fraud_score": float(round(error, 4)),
            "threshold": float(round(fraud_threshold, 4)),
            "transaction": txn.model_dump(by_alias=True)
        }
    except ValueError as ve:
        raise HTTPException(422, detail=str(ve))
    except Exception as e:
        raise HTTPException(500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/high-spender")
def predict_high_spender(txn: Transaction):
    try:
        city_code = int(le_city.transform([txn.City])[0])
        card_code = int(le_card.transform([txn.Card_Type])[0])
        exp_code = int(le_exp.transform([txn.Exp_Type])[0])
        date = pd.to_datetime(txn.Date, format='%d-%b-%y')

        row = np.array([[txn.Amount, date.month, date.day,
                         1 if date.dayofweek >= 5 else 0,
                         city_code, card_code, exp_code]])

        proba = high_spender_model.predict_proba(row)
        prob = float(proba[0][1] if proba.shape[1] == 2 else 0.0)

        return {
            "probability_big_spender": float(round(prob, 4)),
            "recommend_premium": bool(prob > 0.65),
            "transaction": txn.model_dump(by_alias=True)
        }
    except ValueError as ve:
        raise HTTPException(422, detail=str(ve))
    except Exception as e:
        raise HTTPException(500, detail=f"Prediction failed: {str(e)}")

# ────────────────────────────────────────────────
# Customer Profile (with fraud history)
# ────────────────────────────────────────────────
@app.get("/customer/{customer_id}/profile")
def customer_profile(customer_id: int):
    if df is None:
        raise HTTPException(
            status_code=503,
            detail="Customer profile data not available (processed CSV not loaded)"
        )

    cust = df[df['Customer_ID'] == customer_id]
    if cust.empty:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Ensure Date is datetime
    if df['Date'].dtype == 'object':
        df['Date'] = pd.to_datetime(df['Date'])
    cust = df[df['Customer_ID'] == customer_id]

    total_spend = float(cust['Amount'].sum())
    transaction_count = len(cust)
    avg_transaction = float(cust['Amount'].mean())
    last_active = cust['Date'].max().strftime("%Y-%m-%d")
    inactive_days = (pd.Timestamp.today() - cust['Date'].max()).days
    churn_risk = inactive_days > 120

    monthly_avg = cust.set_index('Date').resample('M')['Amount'].sum().mean()
    clv_lakhs = round((monthly_avg * 60) / 100000, 2)

    recommended_limit = round(avg_transaction * 3, -2)

    # Fraud history
    fraud_tx = cust[cust['AE_Fraud'] == 1]
    fraud_count = len(fraud_tx)
    fraud_amount = float(fraud_tx['Amount'].sum()) if not fraud_tx.empty else 0.0
    fraud_pct = round((fraud_count / transaction_count) * 100, 2) if transaction_count > 0 else 0.0
    fraud_common_exp = fraud_tx['Exp Type'].mode()[0] if not fraud_tx.empty else None
    latest_fraud = fraud_tx['Date'].max().strftime("%Y-%m-%d") if not fraud_tx.empty else None

    return {
        "customer_id": customer_id,
        "total_spend": total_spend,
        "total_spend_readable": f"₹{total_spend:,.0f}",
        "transaction_count": transaction_count,
        "average_transaction": round(avg_transaction),
        "last_active_date": last_active,
        "inactive_days": inactive_days,
        "churn_risk": bool(churn_risk),
        "estimated_clv_lakhs": clv_lakhs,
        "recommended_credit_limit": recommended_limit,
        "recommended_limit_readable": f"₹{recommended_limit:,.0f}",

        # Fraud history
        "fraud_count": fraud_count,
        "fraud_total_amount": fraud_amount,
        "fraud_total_readable": f"₹{fraud_amount:,.0f}" if fraud_amount > 0 else "₹0",
        "fraud_percentage": fraud_pct,
        "most_common_fraud_exp_type": fraud_common_exp,
        "latest_fraud_date": latest_fraud
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)