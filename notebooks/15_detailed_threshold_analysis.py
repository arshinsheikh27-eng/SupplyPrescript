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
    confusion_matrix,
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
# 1. Load and sort data
# ---------------------------------------------------------

df = pd.read_csv(DATA_PATH)

df["order_date"] = pd.to_datetime(df["order_date"])

df = (
    df.sort_values("order_date")
    .reset_index(drop=True)
)


# ---------------------------------------------------------
# 2. Chronological train / validation split
# ---------------------------------------------------------

train_full_size = int(len(df) * 0.80)

train_full = df.iloc[:train_full_size]

train_size = int(len(train_full) * 0.80)

train = train_full.iloc[:train_size]
validation = train_full.iloc[train_size:]

X_train = train[FEATURES]
y_train = train[TARGET]

X_validation = validation[FEATURES]
y_validation = validation[TARGET]


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
# 4. Random Forest
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
# 5. Train using training data only
# ---------------------------------------------------------

print("Training Random Forest...")

model.fit(X_train, y_train)


# ---------------------------------------------------------
# 6. Validation probabilities
# ---------------------------------------------------------

probabilities = model.predict_proba(
    X_validation
)[:, 1]


# ---------------------------------------------------------
# 7. Detailed threshold analysis
# ---------------------------------------------------------

thresholds = [
    0.30,
    0.325,
    0.35,
    0.375,
    0.40,
    0.425,
    0.45,
    0.475,
    0.50,
    0.525,
    0.55,
    0.575,
    0.60,
]

results = []

for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_validation,
        predictions
    ).ravel()

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
        "Predicted_Risk_%": (
            predictions.mean() * 100
        ),
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "TP": tp,
    })


results_df = pd.DataFrame(results)


# ---------------------------------------------------------
# 8. Display results
# ---------------------------------------------------------

print("\n" + "=" * 110)
print("DETAILED RANDOM FOREST THRESHOLD ANALYSIS - VALIDATION SET")
print("=" * 110)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# ---------------------------------------------------------
# 9. Highest F1
# ---------------------------------------------------------

best_f1 = results_df.loc[
    results_df["F1"].idxmax()
]

print("\n" + "=" * 70)
print("HIGHEST VALIDATION F1")
print("=" * 70)

print(
    best_f1.to_string()
)


# ---------------------------------------------------------
# 10. Highest precision while maintaining recall >= 0.70
# ---------------------------------------------------------

balanced_candidates = results_df[
    results_df["Recall"] >= 0.70
]

if not balanced_candidates.empty:

    best_balanced = balanced_candidates.loc[
        balanced_candidates["Precision"].idxmax()
    ]

    print("\n" + "=" * 70)
    print("HIGHEST PRECISION WITH RECALL >= 0.70")
    print("=" * 70)

    print(
        best_balanced.to_string()
    )


print("\nImportant:")
print(
    "Threshold analysis uses validation data only."
)

print(
    "The previously evaluated test set is not used "
    "for threshold selection."
)