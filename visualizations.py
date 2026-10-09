import os
import matplotlib.pyplot as plt
import seaborn as sns
from src.config import CHARTS_DIR

def create_charts(results):
    os.makedirs(CHARTS_DIR, exist_ok=True)

    funnel = results["funnel"]
    plt.figure(figsize=(9, 5))
    sns.barplot(data=funnel, x="funnel_stage", y="sessions")
    plt.title("E-Commerce Conversion Funnel")
    plt.xlabel("Funnel Stage")
    plt.ylabel("Unique Sessions")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "funnel_chart.png"), dpi=150)
    plt.close()

    category = results["category"].head(10)
    plt.figure(figsize=(9, 5))
    sns.barplot(data=category, x="revenue", y="category")
    plt.title("Top Categories by Revenue")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "category_revenue.png"), dpi=150)
    plt.close()

    traffic = results["traffic"].sort_values("conversion_rate_pct", ascending=False)
    plt.figure(figsize=(9, 5))
    sns.barplot(data=traffic, x="conversion_rate_pct", y="traffic_source")
    plt.title("Traffic Source Conversion Rate")
    plt.xlabel("Conversion Rate (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "traffic_conversion.png"), dpi=150)
    plt.close()

    daily = results["daily"]
    plt.figure(figsize=(10, 5))
    plt.plot(daily["date"], daily["revenue"])
    plt.title("Daily Revenue Trend")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "daily_revenue.png"), dpi=150)
    plt.close()
