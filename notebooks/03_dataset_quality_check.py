from pathlib import Path
import pandas as pd

# Locate the project and prepared dataset
project_folder = Path(__file__).resolve().parent.parent
input_path = (
    project_folder
    / "data"
    / "processed"
    / "supplyprescript_order_model_data.csv"
)
output_folder = project_folder / "data" / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

print("Loading prepared dataset...")
df = pd.read_csv(input_path)

# 1. Overall dataset checks
print("\n========== DATASET OVERVIEW ==========")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Exact duplicate rows:", df.duplicated().sum())

if "Order Id" in df.columns:
    print("Unique Order Ids:", df["Order Id"].nunique())
    print("Duplicate Order Ids:", df["Order Id"].duplicated().sum())

# 2. Column-level quality report
quality = pd.DataFrame({
    "column": df.columns,
    "data_type": [str(df[col].dtype) for col in df.columns],
    "missing_count": [df[col].isna().sum() for col in df.columns],
    "missing_percent": [
        round(df[col].isna().mean() * 100, 2) for col in df.columns
    ],
    "unique_values": [df[col].nunique(dropna=True) for col in df.columns],
    "constant_column": [df[col].nunique(dropna=True) <= 1 for col in df.columns],
})

quality_path = output_folder / "dataset_quality_by_column.csv"
quality.to_csv(quality_path, index=False)

print("\n========== COLUMN QUALITY ==========")
print(quality.to_string(index=False))

# 3. Numeric-column summaries
numeric = df.select_dtypes(include="number")
if not numeric.empty:
    numeric_summary = numeric.describe().T
    numeric_path = output_folder / "numeric_summary.csv"
    numeric_summary.to_csv(numeric_path)
    print("\n========== NUMERIC SUMMARY ==========")
    print(numeric_summary.to_string())

# 4. Target checks
target = "late_delivery_risk"
if target in df.columns:
    print("\n========== TARGET CHECK ==========")
    print("Target values:", sorted(df[target].dropna().unique().tolist()))
    print("Target distribution:")
    print(df[target].value_counts(dropna=False).sort_index())
    print("Target missing:", df[target].isna().sum())

# 5. Basic business-rule checks
print("\n========== VALUE CHECKS ==========")

if "scheduled_shipping_days" in df.columns:
    print(
        "Scheduled days below zero:",
        (df["scheduled_shipping_days"] < 0).sum()
    )

if "item_count" in df.columns:
    print("Item count zero or below:", (df["item_count"] <= 0).sum())

if "total_quantity" in df.columns:
    print(
        "Total quantity zero or below:",
        (df["total_quantity"] <= 0).sum()
    )

if "total_sales" in df.columns:
    print("Total sales below zero:", (df["total_sales"] < 0).sum())

# 6. Save a compact text report
report_path = output_folder / "dataset_quality_report.txt"

with open(report_path, "w", encoding="utf-8") as report:
    report.write("SUPPLYPRESCRIPT DATASET QUALITY REPORT\n")
    report.write("=====================================\n")
    report.write(f"Rows: {len(df)}\n")
    report.write(f"Columns: {len(df.columns)}\n")
    report.write(f"Exact duplicate rows: {df.duplicated().sum()}\n")
    report.write("\nCOLUMN QUALITY\n")
    report.write(quality.to_string(index=False))
    report.write("\n\nDATA TYPES\n")
    report.write(df.dtypes.to_string())
    report.write("\n\nMISSING VALUES\n")
    report.write(df.isna().sum().to_string())
    if target in df.columns:
        report.write("\n\nTARGET DISTRIBUTION\n")
        report.write(df[target].value_counts(dropna=False).sort_index().to_string())

print("\nSaved quality files:")
print(quality_path)
print(output_folder / "numeric_summary.csv")
print(report_path)