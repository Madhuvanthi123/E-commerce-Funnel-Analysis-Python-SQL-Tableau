import os
import numpy as np
import pandas as pd
from src.config import CLEANED_FILE, REPORTS_DIR

FUNNEL_ORDER = ["visit", "view", "add_to_cart", "checkout", "purchase"]

def run_analysis():
    df = pd.read_excel(CLEANED_FILE)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    funnel = df.groupby("event_type")["session_id"].nunique().reindex(FUNNEL_ORDER, fill_value=0)
    funnel_df = funnel.rename_axis("funnel_stage").reset_index(name="sessions")
    base = max(float(funnel.iloc[0]), 1.0)
    funnel_df["conversion_from_visit_pct"] = np.round(funnel_df["sessions"] / base * 100, 2)
    funnel_df["drop_off_from_previous"] = funnel_df["sessions"].shift(1).fillna(funnel_df["sessions"]) - funnel_df["sessions"]
    funnel_df["drop_off_from_previous"] = funnel_df["drop_off_from_previous"].astype(int)

    purchases = df[df["event_type"] == "purchase"].copy()
    purchases["revenue"] = purchases["price"] * purchases["quantity"]

    category = purchases.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    traffic = df.groupby("traffic_source")["session_id"].nunique().reset_index(name="sessions")
    traffic_p = purchases.groupby("traffic_source")["session_id"].nunique().reset_index(name="purchasing_sessions")
    traffic = traffic.merge(traffic_p, on="traffic_source", how="left").fillna(0)
    traffic["conversion_rate_pct"] = np.round(traffic["purchasing_sessions"] / traffic["sessions"].replace(0, np.nan) * 100, 2).fillna(0)

    products = purchases.groupby(["product_id", "product_name", "category"], as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    daily = purchases.groupby(purchases["event_time"].dt.date, as_index=False)["revenue"].sum()
    daily.columns = ["date", "revenue"]

    kpis = pd.DataFrame({
        "metric": ["Total Sessions", "Total Customers", "Total Purchases", "Total Revenue", "Overall Conversion Rate (%)"],
        "value": [
            int(df["session_id"].nunique()),
            int(df["customer_id"].nunique()),
            int(purchases["session_id"].nunique()),
            round(float(purchases["revenue"].sum()), 2),
            round(float((purchases["session_id"].nunique() / max(df[df["event_type"]=="visit"]["session_id"].nunique(), 1))*100), 2)
        ]
    })

    report_path = os.path.join(REPORTS_DIR, "ecommerce_analysis_report.xlsx")
    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        funnel_df.to_excel(writer, sheet_name="Funnel", index=False)
        category.to_excel(writer, sheet_name="Category Revenue", index=False)
        traffic.to_excel(writer, sheet_name="Traffic Source", index=False)
        products.to_excel(writer, sheet_name="Top Products", index=False)
        daily.to_excel(writer, sheet_name="Daily Revenue", index=False)
        kpis.to_excel(writer, sheet_name="KPIs", index=False)

    return {"funnel": funnel_df, "category": category, "traffic": traffic, "products": products, "daily": daily, "kpis": kpis}