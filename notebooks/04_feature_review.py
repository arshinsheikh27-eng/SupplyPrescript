from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
input_path = (
    project_folder / "data" / "processed"
    / "supplyprescript_order_model_data.csv"
)

df = pd.read_csv(input_path)

target = "late_delivery_risk"

print("========== TARGET BY YEAR ==========")
year_summary = df.groupby("order_year")[target].agg(
    orders="count",
    late_orders="sum",
    late_rate="mean"
)
year_summary["late_rate"] = (year_summary["late_rate"] * 100).round(2)
print(year_summary)

print("\n========== CANDIDATE CATEGORICAL FEATURES ==========")
categorical_cols = [
    "shipping_mode",
    "payment_type",
    "market",
    "order_region",
    "customer_segment",
]

for col in categorical_cols:
    print(f"\n--- {col} ---")
    summary = df.groupby(col, dropna=False)[target].agg(
        orders="count",
        late_rate="mean"
    )
    summary["late_rate"] = (summary["late_rate"] * 100).round(2)
    print(summary.sort_values("orders", ascending=False).to_string())

print("\n========== NUMERIC FEATURE CORRELATIONS ==========")
numeric_cols = [
    "scheduled_shipping_days",
    "item_count",
    "total_quantity",
    "total_sales",
    "distinct_categories",
    "distinct_departments",
    "order_month",
    "order_day_of_week",
    target,
]
print(df[numeric_cols].corr(numeric_only=True)[target].sort_values(
    ascending=False
))

print("\nReview complete.")