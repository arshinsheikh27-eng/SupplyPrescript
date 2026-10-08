import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATA_PATH = "data/processed/supplyprescript_order_model_data.csv"

NUMERIC_FEATURES = [
    "scheduled_shipping_days",
    "item_count",
    "total_quantity",
    "total_sales",
    "distinct_categories",
    "distinct_departments",
    "order_year",
    "order_month",
    "order_day_of_week",
]

CATEGORICAL_FEATURES = [
    "shipping_mode",
    "payment_type",
    "market",
    "order_region",
    "customer_segment",
]


# Load data
df = pd.read_csv(DATA_PATH)

# Sort chronologically
df["order_date"] = pd.to_datetime(df["order_date"])
df = df.sort_values("order_date").reset_index(drop=True)

X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
y = df["late_delivery_risk"]

# Chronological train/validation/test structure
train_full_size = int(len(df) * 0.80)
train_full = df.iloc[:train_full_size]

train_size = int(len(train_full) * 0.80)
train = train_full.iloc[:train_size]

X_train = train[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
y_train = train["late_delivery_risk"]

# Preprocessing
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, NUMERIC_FEATURES),
    ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
])

# Random Forest
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model),
])

print("Training Random Forest...")
pipeline.fit(X_train, y_train)

# Get transformed feature names and importances
feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
importances = pipeline.named_steps["model"].feature_importances_

importance_df = pd.DataFrame({
    "transformed_feature": feature_names,
    "importance": importances
})

# Map transformed features back to original features
def get_original_feature(feature_name):
    feature_name = feature_name.replace("numeric__", "")
    feature_name = feature_name.replace("categorical__", "")

    for feature in NUMERIC_FEATURES + CATEGORICAL_FEATURES:
        if feature_name == feature or feature_name.startswith(feature + "_"):
            return feature

    return feature_name


importance_df["original_feature"] = (
    importance_df["transformed_feature"]
    .apply(get_original_feature)
)

# Group one-hot encoded features
grouped_importance = (
    importance_df
    .groupby("original_feature", as_index=False)["importance"]
    .sum()
    .sort_values("importance", ascending=False)
)

print("\nGrouped Feature Importance:")
print(grouped_importance.to_string(index=False))

print("\nTotal importance:", grouped_importance["importance"].sum())