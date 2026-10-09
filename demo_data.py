import os
import numpy as np
import pandas as pd
from src.config import RAW_DATA_PATH, RAW_DIR

def create_demo_data(rows=3000, seed=42):
    os.makedirs(RAW_DIR, exist_ok=True)
    rng = np.random.default_rng(seed)

    sessions = [f"S{n:05d}" for n in range(1, 801)]
    customers = [f"C{n:05d}" for n in range(1, 601)]
    products = [
        ("P001", "Wireless Headphones", "Electronics", 2499),
        ("P002", "Smart Watch", "Electronics", 3999),
        ("P003", "Running Shoes", "Fashion", 1999),
        ("P004", "Cotton T-Shirt", "Fashion", 799),
        ("P005", "Coffee Maker", "Home", 3499),
        ("P006", "Water Bottle", "Home", 499),
    ]
    sources = ["Organic", "Paid Search", "Social Media", "Email", "Referral"]

    records = []
    event_id = 1
    start = pd.Timestamp("2026-01-01")

    for session in sessions:
        customer = rng.choice(customers)
        source = rng.choice(sources)
        product = products[int(rng.integers(0, len(products)))]
        current = start + pd.Timedelta(days=int(rng.integers(0, 180)),
                                       minutes=int(rng.integers(0, 1440)))

        stages = ["visit"]
        if rng.random() < 0.82: stages.append("view")
        if rng.random() < 0.48: stages.append("add_to_cart")
        if rng.random() < 0.30: stages.append("checkout")
        if rng.random() < 0.22: stages.append("purchase")

        for stage in stages:
            product_id, product_name, category, price = product
            records.append({
                "event_id": f"E{event_id:07d}",
                "customer_id": customer,
                "session_id": session,
                "event_time": current,
                "event_type": stage,
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "price": float(price),
                "quantity": int(rng.integers(1, 4)),
                "traffic_source": source
            })
            event_id += 1
            current += pd.Timedelta(minutes=int(rng.integers(1, 20)))

    df = pd.DataFrame(records).head(rows)
    df.to_csv(RAW_DATA_PATH, index=False)
    return df
