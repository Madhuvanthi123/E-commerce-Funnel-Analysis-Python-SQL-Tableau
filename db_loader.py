import os
from pathlib import Path
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from src.config import CLEANED_FILE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3307")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "Madhu@pumo123"),
        database=os.getenv("MYSQL_DATABASE", "ecommerce_db")
    )

def load_to_mysql():
    df = pd.read_excel(CLEANED_FILE)
    
    # Replace NaN values with None for MySQL compatibility
    df = df.where(pd.notnull(df), None)

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO ecommerce_events (
        event_id, customer_id, session_id, event_time, 
        event_type, product_id, product_name, category, 
        price, quantity, traffic_source
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        customer_id = VALUES(customer_id),
        session_id = VALUES(session_id),
        event_time = VALUES(event_time),
        event_type = VALUES(event_type),
        product_id = VALUES(product_id),
        product_name = VALUES(product_name),
        category = VALUES(category),
        price = VALUES(price),
        quantity = VALUES(quantity),
        traffic_source = VALUES(traffic_source);
    """

    records = []
    for idx, row in df.iterrows():
        # Ensure fallback for mandatory primary key
        event_id = str(row.get('event_id')) if pd.notnull(row.get('event_id')) else f"EVT_{idx}"
        
        # Datetime conversion check
        event_time = row.get('event_time')
        if pd.notnull(event_time):
            event_time = str(event_time)
        else:
            event_time = None

        records.append((
            event_id,
            row.get('customer_id'),
            str(row.get('session_id')) if pd.notnull(row.get('session_id')) else 'UNKNOWN',
            event_time,
            str(row.get('event_type')),
            row.get('product_id'),
            row.get('product_name'),
            row.get('category'),
            row.get('price', 0.0),
            row.get('quantity', 1),
            row.get('traffic_source')
        ))

    cursor.executemany(insert_query, records)
    conn.commit()

    rows_inserted = cursor.rowcount
    cursor.close()
    conn.close()

    return rows_inserted