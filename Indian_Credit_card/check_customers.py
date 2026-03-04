import pandas as pd
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent
csv_file = script_dir / 'processed_transactions.csv'

df = pd.read_csv(csv_file)
print('Sample Customer IDs (first 20):')
print(df['Customer_ID'].unique()[:20])
print(f'\nTotal unique customers: {df["Customer_ID"].nunique()}')
print(f'Total transactions: {len(df)}')
print(f'\nMin Customer ID: {df["Customer_ID"].min()}')
print(f'Max Customer ID: {df["Customer_ID"].max()}')
