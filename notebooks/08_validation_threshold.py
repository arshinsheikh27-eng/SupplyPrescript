import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


# ---------------------------------------------------------
# 1. Load prepared order-level dataset
# ---------------------------------------------------------

DATA_PATH = "data/processed/supplyprescript_order_model_data.csv"

df = pd.read_csv(DATA_PATH)

# Convert order date to datetime
df["order_date"] = pd.to_datetime(df["order_date"])

# Sort chronologically
df = df.sort_values("order_date").reset_index(drop=True)


# ---------------------------------------------------------
# 2. Define target and model features
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
# 3. Create chronological train + test split
# ---------------------------------------------------------

split_index = int(len(df) * 0.80)

X_train_full = X.iloc[:split_index]
y_train_full = y.iloc[:split_index]

X_test = X.iloc[split_index:]
y_test = y.iloc[split_index:]


# ---------------------------------------------------------
# 4. Split training period into train + validation
# ---------------------------------------------------------

validation_index = int(len(X_train_full) * 0.80)

X_train = X_train_full.iloc[:validation_index]
y_train = y_train_full.iloc[:validation_index]

X_validation = X_train_full.iloc[validation_index:]
y_validation = y_train_full.iloc[validation_index:]


print("Dataset split:")
print("Training rows:", len(X_train))
print("Validation rows:", len(X_validation))
print("Test rows:", len(X_test))

print("\nDate ranges:")

print(
    "Training:",
    df["order_date"].iloc[0],
    "to",
    df["order_date"].iloc[validation_index - 1]
)

print(
    "Validation:",
    df["order_date"].iloc[validation_index],
    "to",
    df["order_date"].iloc[split_index - 1]
)

print(
    "Test:",
    df["order_date"].iloc[split_index],
    "to",
    df["order_date"].iloc[-1]
)


# ---------------------------------------------------------
# 5. Build preprocessing pipeline
# ---------------------------------------------------------

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
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
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features)
    ]
)


# ---------------------------------------------------------
# 6. Build Logistic Regression model
# ---------------------------------------------------------

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000
            )
        )
    ]
)


# ---------------------------------------------------------
# 7. Train ONLY on training data
# ---------------------------------------------------------

model.fit(X_train, y_train)


# ---------------------------------------------------------
# 8. Generate validation probabilities
# ---------------------------------------------------------

validation_probability = model.predict_proba(
    X_validation
)[:, 1]


# ---------------------------------------------------------
# 9. Compare thresholds on validation data
# ---------------------------------------------------------

thresholds = [
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60
]

results = []

for threshold in thresholds:

    validation_prediction = (
        validation_probability >= threshold
    ).astype(int)

    results.append(
        {
            "threshold": threshold,
            "accuracy": accuracy_score(
                y_validation,
                validation_prediction
            ),
            "precision": precision_score(
                y_validation,
                validation_prediction,
                zero_division=0
            ),
            "recall": recall_score(
                y_validation,
                validation_prediction,
                zero_division=0
            ),
            "f1": f1_score(
                y_validation,
                validation_prediction,
                zero_division=0
            )
        }
    )


results_df = pd.DataFrame(results)


# ---------------------------------------------------------
# 10. Display validation results
# ---------------------------------------------------------

print("\nValidation Threshold Comparison:")

print(
    results_df.to_string(index=False)
)


# ---------------------------------------------------------
# 11. Display threshold with highest F1
# ---------------------------------------------------------

best_row = results_df.loc[
    results_df["f1"].idxmax()
]

print("\nBest threshold based on validation F1:")

print(
    best_row.to_string()
)