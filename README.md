# E-commerce-Funnel-Analysis-Python-SQL-Tableau
End-to-end e-commerce funnel analysis that tracks customer journeys from visit to purchase, identifies drop-off points, and uses statistical testing and Tableau dashboards to recommend conversion improvements.
# 🛒 E-commerce Funnel Analysis

## 📌 Project Overview
This project analyzes the customer journey of an online store across the stages
of **Visit → Product View → Add to Cart → Checkout → Purchase**. It uses SQL for
data extraction, Python for cleaning, EDA, and statistical testing, and Tableau
for interactive dashboards to pinpoint where users drop off and what drives
conversion.

## 🎯 Business Objectives
- Measure conversion rate at every stage of the funnel
- Identify the biggest drop-off points and their likely causes
- Compare funnel performance by device, traffic source, category, and region
- Test whether differences between segments are statistically significant
- Recommend actions to increase conversion rate and revenue

## 📊 Key Metrics & KPIs
| Metric | Description |
|---|---|
| Stage Conversion Rate | % of users moving from one stage to the next |
| Overall Conversion Rate | Purchasers ÷ total visitors |
| Cart Abandonment Rate | Users who add to cart but do not purchase |
| Drop-off Rate | % of users lost at each stage |
| Average Order Value (AOV) | Revenue ÷ number of orders |
| Revenue per Visitor | Total revenue ÷ total visitors |
| Customer Retention / Repeat Rate | Customers with 2+ orders |

## 🗂️ Dataset
- **Source:** Kaggle (e.g., E-commerce Events History, Olist Brazilian E-commerce) or sample clickstream data
- **Key fields:** user_id, session_id, event_type, product_id, category, price, device, traffic_source, timestamp
- (Update with the exact dataset link and record count)

## 🛠️ Tools & Technologies
| Category | Tools |
|---|---|
| Programming | Python (Pandas, NumPy) |
| Visualization | Matplotlib, Seaborn, Tableau |
| Database | SQL (MySQL / PostgreSQL / SQLite) |
| Statistics | SciPy, Statsmodels |
| Reporting | Excel, Tableau Public |

## 🔄 Project Workflow
1. **Data Collection**: loaded clickstream and order data
2. **Data Cleaning**: removed duplicates, handled nulls, fixed timestamps (Pandas)
3. **SQL Analysis**: funnel stage counts, cohort queries, window functions, CTEs
4. **Exploratory Data Analysis**: user behavior, seasonality, device and channel splits
5. **Funnel Analysis**: stage-wise conversion and drop-off calculation
6. **Statistical Testing**: A/B test style comparisons, chi-square, confidence intervals
7. **Dashboarding**: Excel summaries and an interactive Tableau dashboard
8. **Insights & Recommendations**: documented findings and action plan

## 📐 Statistical Methods Used
- Descriptive statistics (mean, median, std, distributions)
- Chi-square test of independence (device/channel vs. conversion)
- Two-proportion z-test for comparing conversion rates between groups
- t-test / Mann-Whitney U test for order value differences
- Confidence intervals for conversion rates
- Correlation analysis between session behavior and purchase

## 🧮 Sample Code

**SQL: Funnel stage counts**
```sql
SELECT
    COUNT(DISTINCT CASE WHEN event_type = 'view'     THEN user_id END) AS viewed,
    COUNT(DISTINCT CASE WHEN event_type = 'cart'     THEN user_id END) AS added_to_cart,
    COUNT(DISTINCT CASE WHEN event_type = 'checkout' THEN user_id END) AS checkout,
    COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS purchased
FROM events;
```

**Python: Funnel conversion and drop-off**
```python
import pandas as pd
import matplotlib.pyplot as plt

stages = ["view", "cart", "checkout", "purchase"]
counts = [df[df.event_type == s].user_id.nunique() for s in stages]

funnel = pd.DataFrame({"stage": stages, "users": counts})
funnel["conversion_%"] = funnel["users"].pct_change().add(1).mul(100).round(2)
funnel["drop_off_%"] = 100 - funnel["conversion_%"]

plt.barh(funnel["stage"][::-1], funnel["users"][::-1], color="steelblue")
plt.title("E-commerce Conversion Funnel")
plt.show()
```

**Python: Statistical test (mobile vs. desktop conversion)**
```python
from statsmodels.stats.proportion import proportions_ztest

successes = [mobile_purchases, desktop_purchases]
nobs = [mobile_visitors, desktop_visitors]
z_stat, p_value = proportions_ztest(successes, nobs)
print(f"z = {z_stat:.3f}, p-value = {p_value:.4f}")
```

## 📈 Tableau Dashboard Pages
1. **Executive Overview**: headline KPIs, revenue trend, overall conversion
2. **Funnel View**: stage-wise conversion and drop-off visualization
3. **Segment Analysis**: device, traffic source, region, category
4. **Cart Abandonment**: abandonment trends and top abandoned products
5. **Customer Behavior**: new vs. returning users, repeat purchase rate

🔗 **Live Dashboard:** [Tableau Public Link](https://public.tableau.com/your-link)

## 💡 Key Insights
- Replace with your real findings, for example:
- The largest drop-off occurs between Add to Cart and Checkout (XX%)
- Mobile conversion is significantly lower than desktop (p < 0.05)
- Paid-social traffic has high visits but low purchase conversion

## ✅ Recommendations
- Simplify the checkout flow and offer guest checkout
- Add cart-recovery emails and retargeting for abandoned carts
- Optimize mobile page speed and UX
- Shift marketing budget toward high-converting channels

## 📸 Dashboard Preview
![Dashboard](images/dashboard.png)

## 📁 Repository Structure
