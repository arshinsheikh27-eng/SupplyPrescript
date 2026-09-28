from pathlib import Path
import pandas as pd

# Project paths
project_folder = Path(__file__).resolve().parent.parent
input_path = project_folder / "data" / "raw" / "DataCoSupplyChainDataset.csv"
output_folder = project_folder / "data" / "processed"
output_path = output_folder / "supplyprescript_order_model_data.csv"

output_folder.mkdir(parents=True, exist_ok=True)

print("Reading raw dataset...")
df = pd.read_csv(input_path, encoding="latin1")

# Parse order date and derive calendar features
df["_order_date"] = pd.to_datetime(
    df["order date (DateOrders)"],
    errors="coerce"
)

# Aggregate item rows into one row per order
orders = df.groupby("Order Id", as_index=False).agg(
    late_delivery_risk=("Late_delivery_risk", "first"),
    shipping_mode=("Shipping Mode", "first"),
    scheduled_shipping_days=("Days for shipment (scheduled)", "first"),
    order_date=("_order_date", "first"),
    payment_type=("Type", "first"),
    market=("Market", "first"),
    order_region=("Order Region", "first"),
    order_country=("Order Country", "first"),
    order_state=("Order State", "first"),
    order_city=("Order City", "first"),
    customer_segment=("Customer Segment", "first"),
    item_count=("Order Item Id", "size"),
    total_quantity=("Order Item Quantity", "sum"),
    total_sales=("Sales", "sum"),
    distinct_categories=("Category Name", "nunique"),
    distinct_departments=("Department Name", "nunique"),
)

# Calendar features from the order date
orders["order_year"] = orders["order_date"].dt.year
orders["order_month"] = orders["order_date"].dt.month
orders["order_day_of_week"] = orders["order_date"].dt.dayofweek

# Keep Order Id for tracking/grouping only; do not use it as a model feature
orders = orders.drop(columns=["order_date"])

# Put tracking ID first, target last
target = "late_delivery_risk"
tracking_id = "Order Id"
feature_columns = [c for c in orders.columns if c not in [tracking_id, target]]
orders = orders[[tracking_id] + feature_columns + [target]]

# Basic validation
print("\nPrepared dataset shape:", orders.shape)
print("Unique Order Ids:", orders[tracking_id].nunique())
print("Duplicate Order Ids:", orders[tracking_id].duplicated().sum())
print("\nMissing values by column:")
print(orders.isna().sum())
print("\nTarget distribution:")
print(orders[target].value_counts(dropna=False).sort_index())
print("\nPrepared columns:")
print(orders.columns.tolist())
print("\nSample rows:")
print(orders.head(5).to_string(index=False))

orders.to_csv(output_path, index=False)
print("\nSaved prepared dataset to:", output_path)