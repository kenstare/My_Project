# Indian Credit Card Analysis - Complete Technical Documentation

## Executive Summary

This folder contains exploratory analysis, preprocessing scripts, and a dashboard for Indian credit card transactions. The code loads raw transaction CSV(s), performs cleaning and feature engineering, produces a `processed_transactions.csv` artifact, and builds visualizations including a geographic map export.

In plain English: use the notebook to explore patterns and the scripts to reproduce the preprocessing and dashboard outputs.

---

## How It Works - The Complete Flow

### Phase 1: Data Ingestion
- Raw CSV files are read from the folder or `data/` subfolder into `pandas.DataFrame` objects. Basic validation checks ensure required columns (transaction id, customer id, amount, date/time) are present.

### Phase 2: Cleaning & Enrichment
- Cleaning steps typically include parsing timestamps, filling or removing missing values, normalizing categorical values (merchant categories, locations), removing implausible transactions (negative amounts), and deduplicating records.

### Phase 3: Feature Engineering
- Derive features such as transaction counts per customer, total spend per period, average ticket size, time-of-day buckets, and geographic summarizations (e.g., city or region-level aggregates).

### Phase 4: Export Preprocessed Data
- `main.py` generates `processed_transactions.csv` — the canonical cleaned dataset used by visualizations and further modeling.

### Phase 5: Visualization & Dashboard
- `final_dashboard.py` builds or serves a dashboard (may use Streamlit, Dash, or a static HTML exporter). Geographic visualizations are exported as `india_credit_map.html` for sharing.

---

## Technical Architecture

### Technology Stack (typical)

| Component | Libraries | Purpose |
|-----------|----------|---------|
| Data wrangling | `pandas`, `numpy` | Loading and cleaning data |
| Visualization | `plotly`, `folium`, `geopandas` | Charts and maps |
| Dashboard | `streamlit` or `dash` (if present) | Interactive reporting |
| Scripting | Plain Python scripts | Reproducible preprocessing |

### Key Data Structures
1. Raw DataFrame — original transaction rows
2. Processed DataFrame — cleaned and feature-engineered dataset
3. Aggregates — grouped summaries used by the dashboard (per-customer, per-region)

---

## What Each Code/File Does

- `Eda.ipynb`: Interactive notebook for initial data exploration: distributions, top merchants, time-series of transaction volume, and data-quality checks.

- `check_customers.py`: Utility script to inspect and filter customer records. Example uses:
	- Identify customers with too few transactions
	- Sample high-activity customers for manual review
	- Produce quick reports (CSV or console) about customer segments

- `main.py`: Primary preprocessing pipeline. Typical tasks:
	- Load raw data from `data/` or CSV files
	- Apply cleaning rules (timestamp parsing, drop nulls, remove bad rows)
	- Derive features and aggregations
	- Save `processed_transactions.csv`

- `final_dashboard.py`: Builds or serves the dashboard. Behaviors may include:
	- Starting a local web server (Streamlit/Dash/Flask)
	- Saving a static HTML map report (`india_credit_map.html`)

- `processed_transactions.csv`: Output of `main.py` — the cleaned dataset used for charts and modeling.

- `india_credit_map.html`: Static HTML export of geographic visualization — open in a browser.

- `Credit card transactions - India - Simple.csv` / `data/`: Raw source files — do not overwrite.

---

## Files in this Folder

| File/Folder | Purpose |
|-------------|---------|
| `Eda.ipynb` | Exploratory analysis and visualizations |
| `check_customers.py` | Helper for customer-level checks and sampling |
| `main.py` | Preprocessing and feature engineering pipeline |
| `processed_transactions.csv` | Cleaned data artifact produced by `main.py` |
| `final_dashboard.py` | Script to create or run the dashboard |
| `india_credit_map.html` | Standalone map visualization |

---

## How to Use

### Initial Setup
1. From the repository root, create and activate a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Ensure raw CSV files exist in this folder or `data/`.

### Running the Notebook
- Open `Eda.ipynb` to explore data interactively.

### Reproducible Preprocessing
- Run preprocessing and generate the processed dataset:

```powershell
cd Indian_Credit_card
python check_customers.py
python main.py
```

### Launching the Dashboard / Map
- To preview or serve the dashboard:

```powershell
python final_dashboard.py
```

If the script starts a server, open the printed URL or open `india_credit_map.html` for the static map.

---

## System Capabilities & Limitations

### Capabilities
- Clean and transform raw credit card data
- Produce per-customer and per-region aggregates
- Generate visual dashboards and map exports

### Limitations
- Not a production-grade pipeline (no scheduling, monitoring, or scalable data ingestion)
- Geospatial visualizations may require extra packages (`geopandas`, `shapely`) not present by default

---

## Security & Privacy

- Transactional data may be sensitive. Do not commit raw CSVs containing personally identifiable information.
- Mask or anonymize customer identifiers before sharing outputs.

---

## Summary for Stakeholders

This folder enables fast exploratory analysis and reporting for Indian credit card transactions. Use the notebook for discovery and `main.py` + `final_dashboard.py` for reproducible outputs and shareable visual reports.

What each code/file does
-
- `Eda.ipynb`: Notebook that explores the raw credit card transactions, inspects distributions, plots time-based and categorical summaries, and documents initial findings and assumptions.
- `check_customers.py`: Utility script that filters or validates customer records. Common tasks include identifying customers with many transactions, removing low-activity accounts, or producing a small sample for manual review. It typically reads the raw CSV and writes a report or filtered CSV.
- `main.py`: Main pipeline script. Usually orchestrates data loading, cleaning, feature engineering, and saving the processed dataset to `processed_transactions.csv`. This is the script to run for reproducible preprocessing.
- `final_dashboard.py`: Builds or serves the dashboard. It may start a lightweight web server (e.g., Flask, Streamlit) or generate a static HTML report. If it starts a server, it will print a URL to open in a browser.
- `processed_transactions.csv`: Preprocessed dataset produced by `main.py` used for visualizations and further modeling.
- `india_credit_map.html`: Exported visualization (HTML) showing geographic patterns of transactions; open in a browser to view.
- `Credit card transactions - India - Simple.csv` and `data/`: Raw input data. Keep original copies in `data/` and point scripts to that path.
- `text.txt`: Notes or a README-style quick note maintained by the author; not required to run scripts.

