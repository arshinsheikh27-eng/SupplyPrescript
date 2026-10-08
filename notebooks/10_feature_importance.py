import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier


# ---------------------------------------------------------
# 1. Load prepared dataset
# ---------------------------------------------------------

DATA_PATH = "data/processed/supplyprescript_order_model_data.csv"

df = pd.read_csv(DATA_PATH)

df["order_date"] = pd.to_datetime(df["order_date"])

df = df.sort_values("order_date").reset_index(drop=True)


# ---------------------------------------------------------
# 2. Define target and features
# ---------------------------------------------------------

target = "late_delivery_risk"

numeric_features = [
    "scheduled_shipping_days",
    "item_count",
    "total_quantity",
    "total_sales",
    "distinct_categories",
    "distinct_departments",
    "order_year",
    "order_month",
    "order_day_of_week"
]

categorical_features = [
    "shipping_mode",
    "payment_type",
    "market",
    "order_region",
    "customer_segment"
]

features = numeric_features + categorical_features

X = df[features]
y = df[target]


# ---------------------------------------------------------
# 3. Chronological training split
# ---------------------------------------------------------

test_split = int(len(df) * 0.80)

X_train_full = X.iloc[:test_split]
y_train_full = y.iloc[:test_split]

validation_split = int(len(X_train_full) * 0.80)

X_train = X_train_full.iloc[:validation_split]
y_train = y_train_full.iloc[:validation_split]


# ---------------------------------------------------------
# 4. Preprocessing
# ---------------------------------------------------------

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_features
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    ]
)


# ---------------------------------------------------------
# 5. Random Forest
# ---------------------------------------------------------

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=200,
                max_depth=12,
                min_samples_leaf=5,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


# ---------------------------------------------------------
# 6. Train model
# ---------------------------------------------------------

print("Training Random Forest...")

model.fit(X_train, y_train)


# ---------------------------------------------------------
# 7. Get transformed feature names
# ---------------------------------------------------------

feature_names = (
    model.named_steps["preprocessor"]
    .get_feature_names_out()
)


# ---------------------------------------------------------
# 8. Get feature importance
# ---------------------------------------------------------

importances = (
    model.named_steps["classifier"]
    .feature_importances_
)


importance_df = pd.DataFrame(
    {
        "feature": feature_names,
        "importance": importances
    }
)


# ---------------------------------------------------------
# 9. Sort by importance
# ---------------------------------------------------------

importance_df = importance_df.sort_values(
    "importance",
    ascending=False
)


# ---------------------------------------------------------
# 10. Display top 20
# ---------------------------------------------------------

print("\nTop 20 Model Features:")

print(
    importance_df.head(20).to_string(index=False)
)