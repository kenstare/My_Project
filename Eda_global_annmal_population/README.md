EDA & Forecast: Global Population

Purpose
-
This folder contains exploratory analysis and a simple forecasting workflow for world population data (CSV provided).

Files of interest
-
- `World_Population_Forecast_2023_2100.csv` — dataset used for analysis.
- `eda.ipynb` — Jupyter notebook with exploratory plots and analysis steps.
- `main.py` — script that runs the primary data processing and forecast pipeline (simple usage documented below).

How to run
-
1. From the repository root activate your virtual environment and install dependencies (see root README).
2. To run the notebook, open `eda.ipynb` in Jupyter or VS Code.
3. To run the script version (simple flow):

   ```powershell
   cd Eda_global_annmal_population
   python main.py
   ```

Notes
-
- The notebook is the best starting point to see visualizations and step-by-step reasoning.
- If `main.py` accepts command-line options, run `python main.py --help` to see them.
