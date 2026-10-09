"""
E-Commerce Funnel Analysis — single entry point.

Run order:
  1. Clean raw CSV -> data/processed/ecommerce_cleaned.xlsx (+ Tableau file)
  2. Analyze cleaned data -> outputs/reports/ecommerce_analysis_report.xlsx
  3. Generate charts -> outputs/charts/*.png
  4. Load cleaned data into MySQL (via MySQL Workbench-created schema)

Usage:
    python main.py            # full pipeline including MySQL load
    python main.py --no-db    # skip the MySQL load step
"""

import sys

from src.data_cleaning import clean_ecommerce_data
from src.data_analysis import run_analysis
from src.visualizations import create_charts


def main():
    skip_db = "--no-db" in sys.argv

    print("[1/4] Cleaning raw data...")
    df = clean_ecommerce_data()
    print(f"      -> {len(df)} rows cleaned")

    print("[2/4] Running analysis...")
    results = run_analysis()
    print("      -> report written to outputs/reports/ecommerce_analysis_report.xlsx")

    print("[3/4] Generating charts...")
    create_charts(results)
    print("      -> charts written to outputs/charts/")

    if skip_db:
        print("[4/4] Skipping MySQL load (--no-db flag set).")
    else:
        print("[4/4] Loading into MySQL...")
        try:
            from src.db_loader import load_to_mysql
            inserted = load_to_mysql()
            print(f"      -> {inserted} rows loaded into EcommerceFunnelDB.ecommerce_events")
        except Exception as e:
            print("      !! Could not load into MySQL:", e)
            print("      Check that:")
            print("        - MySQL Workbench / server is running")
            print("        - You ran sql/01_create_database.sql, 02_create_tables.sql, 03_create_views.sql")
            print("        - Your .env file has the correct MYSQL_HOST/PORT/USER/PASSWORD")
            sys.exit(1)

    print("\nDone. E-Commerce Funnel Analysis completed successfully.")


if __name__ == "__main__":
    main()
