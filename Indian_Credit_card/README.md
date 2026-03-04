Indian Credit Card Transactions — README

Purpose
-
This folder contains data and scripts for analyzing credit card transactions in India, plus a dashboard artifact.

Key files
-
- `Credit card transactions - India - Simple.csv` (or under `data/`) — raw transactions dataset.
- `Eda.ipynb` — exploratory notebook showing data insights and visualizations.
- `check_customers.py` — helper script for customer checks/filters.
- `main.py` — primary script to run data processing or analysis pipeline.
- `final_dashboard.py` — script that builds/runs the final dashboard (open it or run to view dashboard).
- `india_credit_map.html` — exported HTML visualization of geographic results.

How to run
-
1. Activate virtual environment and install dependencies.
2. Open `Eda.ipynb` to view the exploratory analysis.
3. Run the main scripts from this folder:

   ```powershell
   cd Indian_Credit_card
   python check_customers.py
   python main.py
   python final_dashboard.py
   ```

4. If `final_dashboard.py` starts a web app, open the printed URL in a browser. If it's a static export, open `india_credit_map.html`.

Notes
-
- Inspect `processed_transactions.csv` to see preprocessed data output.
- Use `python script.py --help` on any script to view available options.
