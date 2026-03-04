Predicting_food_price_nigearia - Documentation

# Predicting Food Price — Nigeria - Complete Technical Documentation

## Executive Summary

This folder contains data, preprocessing, trained-model artifacts, and a small API for predicting food prices in Nigeria. It includes exploratory notebooks, saved artifacts used for inference, and a lightweight prediction endpoint.

In plain English: the notebook documents how the model was developed; the `artifacts/` folder stores the saved encoders and model files; `api.py` loads those artifacts to serve predictions.

---

## How It Works - The Complete Flow

### Phase 1: Data Loading
- The pipeline reads raw or processed CSVs (e.g., `data_processed.csv`) and inspects feature distributions. Data is loaded into `pandas.DataFrame` for cleaning and training.

### Phase 2: Preprocessing & Feature Engineering
- Steps commonly include encoding categorical features using mappings saved in `cat_mapping.joblib`, aligning input feature columns to the model's expected order (`columns.joblib`), imputing missing values, and scaling or transforming numeric features if required.

### Phase 3: Model Training (not always re-run)
- The project stores trained models in `artifacts/` (e.g., `price_model.joblib`). If you retrain, training includes splitting data, fitting the chosen estimator, evaluating performance, and persisting artifacts.

### Phase 4: Serving Predictions
- `api.py` loads `artifacts/` and provides an HTTP endpoint to accept input data, apply the same preprocessing chain, run the model, and return predicted prices as JSON.

### Phase 5: Postprocessing & Outputs
- Optionally apply inflation adjustment using `inflation_model.joblib` or simple scaling, then return/record the final predicted price.

---

## Technical Architecture

### Technology Stack

| Component | Libraries | Purpose |
|-----------|----------|---------|
| Data handling | `pandas`, `numpy` | Load and preprocess data |
| ML models | `scikit-learn`, `xgboost` (optional) | Model training and prediction |
| Model persistence | `joblib` | Save/load preprocessing and model artifacts |
| API | `Flask` or `FastAPI` (if present) | Serve predictions |

### Key Data Structures
1. Training DataFrame — processed training dataset
2. `cat_mapping.joblib` — dict or encoder objects for categorical variables
3. `columns.joblib` — ordered list of feature names expected by the model
4. `price_model.joblib` — trained estimator used for inference

---

## What Each Code/File Does

- `Eda_predicting_food_price_nigeria.ipynb`: Notebook documenting exploratory data analysis, baseline model experiments, feature selection rationale, and evaluation metrics.

- `artifacts/price_model.joblib`: Serialized model used to predict food prices.

- `artifacts/cat_mapping.joblib`: Encoders or mapping dictionaries used to convert categorical inputs into numeric codes consistent with training.

- `artifacts/columns.joblib`: Saved ordered feature list — ensures the API assembles input vectors in the same order used during training.

- `artifacts/inflation_model.joblib` (optional): Model or scaler used to adjust predictions for inflation or market adjustments.

- `artifacts/data_processed.csv`: Example processed dataset used for training and quick sanity checks.

- `api.py`: Lightweight web server that:
  - Loads `cat_mapping.joblib` and `columns.joblib` and `price_model.joblib` on startup
  - Accepts input (JSON or form data), applies preprocessing, orders features, and calls the model's `predict` method
  - Returns predictions as JSON and may log inputs/outputs for debugging

---

## Files in this Folder

| File/Folder | Purpose |
|-------------|---------|
| `Eda_predicting_food_price_nigeria.ipynb` | Notebook for EDA and model experiments |
| `api.py` | Prediction API for serving the trained model |
| `artifacts/` | Saved encoders, column lists, models, and example processed data |

---

## How to Use

### Initial Setup
1. From repo root, create and activate a Python virtual environment and install requirements:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Ensure `artifacts/` contains `price_model.joblib`, `columns.joblib`, and `cat_mapping.joblib`.

### Running the Notebook
- Open `Eda_predicting_food_price_nigeria.ipynb` to reproduce analysis and training experiments.

### Running the API Locally
- To serve predictions:

```powershell
cd Predicting_food_price_nigearia
python api.py
```

Check console output for the listening port and POST example; then call the endpoint with JSON input matching the expected columns.

---

## System Capabilities & Limitations

### Capabilities
- Serve model predictions for new inputs using saved artifacts
- Reproduce training experiments in the notebook
- Provide reproducible preprocessing via saved encoders and column lists

### Limitations
- Model artifacts are static; to update predictions you must retrain and replace `artifacts/` files
- API is lightweight and not production hardened (no auth, rate limiting, or monitoring)

---

## Security & Operational Considerations

- Do not commit `artifacts/` with sensitive data to public repos if it contains training data traces.
- The API should be run behind authenticated infrastructure for production use; rotate keys and secure the hosting environment.

---

## Machine Learning Concepts (brief)

- Categorical encodings must be consistent between training and inference — that is why `cat_mapping.joblib` is stored and re-used by `api.py`.
- Column ordering matters for many models; `columns.joblib` preserves the exact feature order used during training.

---

## Summary for Stakeholders

This folder contains a runnable prediction pipeline: artifacts for offline inference, a documented notebook showing model development, and an API to serve predictions. It is suitable for prototyping and evaluation; production deployment requires further hardening and monitoring.


What each code/file does
-
- `Eda_predicting_food_price_nigeria.ipynb`: Notebook used for data exploration, feature engineering experiments, and model training. It documents chosen features, preprocessing steps, model selection, and evaluation results.
- `api.py`: Small web API to serve predictions. Typical flow:
  - Load artifact files from `artifacts/` (`columns.joblib`, `cat_mapping.joblib`, `price_model.joblib`, etc.)
  - Receive input (JSON or form data)
  - Apply the same preprocessing used at training time (categorical mappings, column ordering)
  - Run `price_model` to predict prices
  - Return predictions as JSON
  Run `python api.py` to start the server (check console for URL/port).
- `artifacts/price_model.joblib`: Saved model used for price prediction.
- `artifacts/inflation_model.joblib`: Optional model to adjust predictions for inflation or other external factors.
- `artifacts/cat_mapping.joblib`: Mapping of categorical variables (label encoders or dicts) used during preprocessing—must be loaded by `api.py`.
- `artifacts/columns.joblib`: Ordered list of feature columns expected by the model; ensures input vectors match training order.
- `artifacts/data_processed.csv`: Example processed dataset used during training and for quick sanity-checks.

