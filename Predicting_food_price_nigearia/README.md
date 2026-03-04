Predicting Food Price — Nigeria

Purpose
-
This folder contains data, trained models, and a small API for predicting food prices in Nigeria.

Files of interest
-
- `Eda_predicting_food_price_nigeria.ipynb` — exploratory notebook for feature exploration and model experiments.
- `artifacts/` — contains trained models and metadata (`cat_mapping.joblib`, `columns.joblib`, `inflation_model.joblib`, `price_model.joblib`, `data_processed.csv`).
- `api.py` — small API to serve predictions using the artifact models.

How to run
-
1. Activate the virtual environment and install dependencies.
2. Inspect the notebook to see model training and preprocessing details.
3. To run the API locally:

   ```powershell
   cd Predicting_food_price_nigearia
   python api.py
   ```

   - The API will load models from the `artifacts/` folder. Check the console output for the serving URL/port.
4. To run analysis or reproduce results, open `Eda_predicting_food_price_nigeria.ipynb`.

Notes
-
- If the API uses Flask or FastAPI, you may need to install optional dependencies; check `requirements.txt`.
- Keep the `artifacts` folder intact — it contains the saved preprocessing and model objects.
