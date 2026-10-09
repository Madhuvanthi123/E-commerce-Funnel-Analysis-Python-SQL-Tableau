"""Quick sanity check: confirms Python can reach your MySQL Workbench database
using the credentials in your .env file. Run this first before main.py."""

from pathlib import Path
import os
import mysql.connector
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

try:
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3307")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD","Madhu@pumo123"),
        database=os.getenv("MYSQL_DATABASE", "ecommerce_db"),
    )

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")

    print("Connected successfully!")
    print("Tables found in database:", cursor.fetchall())

    cursor.close()
    connection.close()

except mysql.connector.Error as err:
    print(f"Connection failed: {err}")