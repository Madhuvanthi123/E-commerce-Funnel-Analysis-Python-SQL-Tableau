import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Define CLEANED_FILE here
CLEANED_FILE = PROCESSED_DATA_DIR / "ecommerce_cleaned.xlsx"

OUTPUTS_DIR = BASE_DIR / "outputs"
CHARTS_DIR = OUTPUTS_DIR / "charts"
REPORTS_DIR = OUTPUTS_DIR / "reports"

# Database config
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Madhu@pumo123")
DB_NAME = os.getenv("DB_NAME", "ecommerce_db")
DB_PORT = int(os.getenv("DB_PORT", 3307))