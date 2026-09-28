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