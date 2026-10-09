import pandas as pd
import os
from src.config import RAW_DATA_DIR, CLEANED_FILE, PROCESSED_DATA_DIR

def clean_ecommerce_data(df: pd.DataFrame = None) -> pd.DataFrame:
    # 1. Load data if no DataFrame was provided directly
    if df is None:
        raw_csv_path = RAW_DATA_DIR / "ecommerce_events.csv"
        df = pd.read_csv(raw_csv_path)

    df = df.copy()

    # 2. Data Cleaning steps
    if 'event_time' in df.columns:
        df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')

    if 'user_id' in df.columns:
        df['user_id'] = df['user_id'].fillna('UNKNOWN')

    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)

    if 'event_type' in df.columns:
        df = df.dropna(subset=['event_type'])

    # 3. Save cleaned file for analysis and downstream steps
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    df.to_excel(CLEANED_FILE, index=False)

    return df