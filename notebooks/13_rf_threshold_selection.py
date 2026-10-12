import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


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

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "late_delivery_risk"


# ---------------------------------------------------------
# 1. Load and sort data chronologically
# ---------------------------------------------------------

df = pd.read_csv(DATA_PATH)

df["order_date"] = pd.to_datetime(df["order_date"])

df = (
    df.sort_values("order_date")
    .reset_index(drop=True)
)


# ---------------------------------------------------------
# 2. Chronological train / validation / test split
# ---------------------------------------------------------

train_full_size = int(len(df) * 0.80)

train_full = df.iloc[:train_full_size]
validation_test = df.iloc[train_full_size:]

train_size = int(len(train_full) * 0.80)

train = train_full.iloc[:train_size]
validation = train_full.iloc[train_size:]

X_train = train[FEATURES]
y_train = train[TARGET]

X_validation = validation[FEATURES]
y_validation = validation[TARGET]


print("Training rows   :", len(train))
print("Validation rows:", len(validation))

print("\nTraining dates:")
print(train["order_date"].min(), "to", train["order_date"].max())

print("\nValidation dates:")
print(
    validation["order_date"].min(),
    "to",
    validation["order_date"].max()
)


# ---------------------------------------------------------
# 3. Random Forest preprocessing
# ---------------------------------------------------------

preprocessor = ColumnTransformer([
    (
        "numeric",
        Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
        ]),
        NUMERIC_FEATURES,
    ),
    (
        "categorical",
        Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]),
        CATEGORICAL_FEATURES,
    ),
])


# ---------------------------------------------------------
# 4. Random Forest model
# ---------------------------------------------------------

model = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "classifier",
        RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        )
    ),
])


# ---------------------------------------------------------
# 5. Train on training data only
# ---------------------------------------------------------

print("\nTraining Random Forest...")

model.fit(X_train, y_train)


# ---------------------------------------------------------
# 6. Get validation probabilities
# ---------------------------------------------------------

validation_probabilities = model.predict_proba(
    X_validation
)[:, 1]


# ---------------------------------------------------------
# 7. Evaluate candidate thresholds
# ---------------------------------------------------------

thresholds = [
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
]

results = []

for threshold in thresholds:

    predictions = (
        validation_probabilities >= threshold
    ).astype(int)

    results.append({
        "Threshold": threshold,
        "Accuracy": accuracy_score(
            y_validation,
            predictions
        ),
        "Precision": precision_score(
            y_validation,
            predictions,
            zero_division=0
        ),
        "Recall": recall_score(
            y_validation,
            predictions,
            zero_division=0
        ),
        "F1": f1_score(
            y_validation,
            predictions,
            zero_division=0
        ),
    })


results_df = pd.DataFrame(results)


# ---------------------------------------------------------
# 8. Display results
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("RANDOM FOREST THRESHOLD ANALYSIS - VALIDATION SET")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}"
    )
)


# ---------------------------------------------------------
# 9. Identify highest validation F1
# ---------------------------------------------------------

best_row = results_df.loc[
    results_df["F1"].idxmax()
]

print("\n" + "=" * 70)
print("BEST VALIDATION F1")
print("=" * 70)

print(
    f"Threshold : {best_row['Threshold']:.2f}"
)

print(
    f"Accuracy  : {best_row['Accuracy']:.6f}"
)

print(
    f"Precision : {best_row['Precision']:.6f}"
)

print(
    f"Recall    : {best_row['Recall']:.6f}"
)

print(
    f"F1        : {best_row['F1']:.6f}"
)


print("\nImportant:")
print(
    "Threshold selection is based only on the validation set. "
    "The final test set remains untouched."
)