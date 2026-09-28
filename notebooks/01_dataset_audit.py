from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "raw" / "DataCoSupplyChainDataset.csv"

print("CSV path:", file_path)
print("File exists:", file_path.exists())

df = pd.read_csv(file_path, encoding="latin1")

# Show basic information
print("Dataset loaded successfully!")
print("Rows and columns:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types and non-null counts:")
df.info()

print("\nMissing values in each column:")
print(df.isna().sum().sort_values(ascending=False))

print("\nDuplicate rows:")
print(df.duplicated().sum())

# Check whether the target column exists
target = "Late_delivery_risk"

print("\nTarget column check:")
if target in df.columns:
    print(df[target].value_counts(dropna=False))
else:
    print("Target column not found. Check the exact spelling.") 

# Check whether each row is an order item or a unique order
print("\nRow-granularity checks:")
print("Unique Order Ids:", df["Order Id"].nunique())
print("Unique Order Item Ids:", df["Order Item Id"].nunique())

# Check the target against delivery outcome-related fields
print("\nTarget by Delivery Status:")
print(pd.crosstab(
    df["Delivery Status"],
    df["Late_delivery_risk"],
    margins=True
))

print("\nReal vs scheduled shipping days:")
print(pd.crosstab(
    df["Days for shipping (real)"],
    df["Days for shipment (scheduled)"]
).head(10))

# Check date range
df["order date (DateOrders)"] = pd.to_datetime(
    df["order date (DateOrders)"],
    errors="coerce"
)
print("\nOrder date range:")
print(df["order date (DateOrders)"].min(),
      "to",
      df["order date (DateOrders)"].max())

# Inspect key categorical values and possible data issues
check_cols = [
    "Type",
    "Shipping Mode",
    "Delivery Status",
    "Late_delivery_risk",
    "Order Status",
    "Product Status",
    "Customer Segment",
    "Market"
]

for col in check_cols:
    if col in df.columns:
        print(f"\n--- {col} ---")
        print(df[col].value_counts(dropna=False).head(15))

# Check whether scheduled shipping days has unusual values
print("\nScheduled shipping days distribution:")
print(df["Days for shipment (scheduled)"].value_counts(dropna=False).sort_index())

# Check missingness in columns we may consider keeping
candidate_cols = [
    "Type",
    "Days for shipment (scheduled)",
    "Shipping Mode",
    "order date (DateOrders)",
    "Market",
    "Order Region",
    "Order Country",
    "Order City",
    "Customer Segment",
    "Category Name",
    "Order Item Quantity",
    "Order Item Product Price",
    "Late_delivery_risk"
]

print("\nMissing values in candidate columns:")
print(df[candidate_cols].isna().sum())

# 1. Verify record identifiers
print("Unique Order Item Ids:", df["Order Item Id"].nunique())
print("Rows:", len(df))
print("Duplicate Order Item Ids:", df["Order Item Id"].duplicated().sum())

# 2. Check target values
print("\nTarget values:", sorted(df["Late_delivery_risk"].dropna().unique()))

# 3. Check whether the order date parses correctly
order_dates = pd.to_datetime(
    df["order date (DateOrders)"],
    errors="coerce"
)
print("\nUnparseable order dates:", order_dates.isna().sum())
print("Earliest order date:", order_dates.min())
print("Latest order date:", order_dates.max())

# 4. Compare target to actual-vs-scheduled delay
late_by_days = (
    df["Days for shipping (real)"] >
    df["Days for shipment (scheduled)"]
)
print("\nTarget vs actual delay comparison:")
print(pd.crosstab(
    df["Late_delivery_risk"],
    late_by_days,
    rownames=["Late_delivery_risk"],
    colnames=["Actual days > scheduled days"],
    margins=True
))
print(
    "Rows where target disagrees with actual > scheduled:",
    (df["Late_delivery_risk"] != late_by_days.astype(int)).sum()
)

# Check whether shipment details are consistent within each Order Id
shipment_fields = [
    "Late_delivery_risk",
    "Shipping Mode",
    "Days for shipment (scheduled)",
    "order date (DateOrders)",
    "Order Country",
    "Order Region",
    "Order State",
    "Order City",
]

order_variation = df.groupby("Order Id")[shipment_fields].nunique()

print("\nOrders with more than one value in shipment fields:")
for column in shipment_fields:
    count = (order_variation[column] > 1).sum()
    print(f"{column}: {count}")

print("\nTotal unique orders:", df["Order Id"].nunique())