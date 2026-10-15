import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATA_PATH = "data/processed/supplyprescript_order_model_data.csv"

OUTPUT_PATH = "data/processed/final_test_predictions_threshold_040.csv"

FINAL_THRESHOLD = 0.40


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
# 2. Recreate chronological split
# ---------------------------------------------------------

train_full_size = int(len(df) * 0.80)

train_full = df.iloc[:train_full_size]
test = df.iloc[train_full_size:].copy()

X_train_full = train_full[FEATURES]
y_train_full = train_full[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]


print("Training + Validation rows:", len(train_full))
print("Test rows:", len(test))

print("\nTraining + Validation dates:")
print(
    train_full["order_date"].min(),
    "to",
    train_full["order_date"].max()
)

print("\nTest dates:")
print(
    test["order_date"].min(),
    "to",
    test["order_date"].max()
)


# ---------------------------------------------------------
# 3. Preprocessing
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
# 4. Final Random Forest
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
# 5. Train on train + validation
# ---------------------------------------------------------

print("\nTraining final Random Forest...")

model.fit(
    X_train_full,
    y_train_full
)


# ---------------------------------------------------------
# 6. Generate probabilities
# ---------------------------------------------------------

test_probabilities = model.predict_proba(
    X_test
)[:, 1]


# ---------------------------------------------------------
# 7. Apply selected threshold
# ---------------------------------------------------------

test_predictions = (
    test_probabilities >= FINAL_THRESHOLD
).astype(int)


# ---------------------------------------------------------
# 8. Metrics
# ---------------------------------------------------------

accuracy = accuracy_score(
    y_test,
    test_predictions
)

precision = precision_score(
    y_test,
    test_predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    test_predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    test_predictions,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    test_probabilities
)

cm = confusion_matrix(
    y_test,
    test_predictions
)

tn, fp, fn, tp = cm.ravel()


# ---------------------------------------------------------
# 9. Display results
# ---------------------------------------------------------

print("\n" + "=" * 75)
print("TEST EVALUATION - RANDOM FOREST - THRESHOLD 0.40")
print("=" * 75)

print("Model     : Random Forest")
print(f"Threshold : {FINAL_THRESHOLD:.2f}")

print(f"\nAccuracy  : {accuracy:.6f}")
print(f"Precision : {precision:.6f}")
print(f"Recall    : {recall:.6f}")
print(f"F1 Score  : {f1:.6f}")
print(f"ROC-AUC   : {roc_auc:.6f}")

print("\nConfusion Matrix:")
print(cm)

print("\nConfusion Matrix Counts:")
print(f"True Negatives  : {tn}")
print(f"False Positives : {fp}")
print(f"False Negatives : {fn}")
print(f"True Positives  : {tp}")

print(
    f"\nPredicted Risk % : "
    f"{test_predictions.mean() * 100:.2f}%"
)


# ---------------------------------------------------------
# 10. Save predictions
# ---------------------------------------------------------

final_predictions = pd.DataFrame({
    "Order Id": test["Order Id"].values,
    "order_date": test["order_date"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
    "late_delivery_risk": y_test.values,
    "predicted_risk": test_predictions,
    "predicted_probability": test_probabilities,
})

final_predictions.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nPredictions saved to: {OUTPUT_PATH}"
)


# ---------------------------------------------------------
# 11. Prediction distribution
# ---------------------------------------------------------

print("\nPrediction distribution:")

print(
    final_predictions["predicted_risk"]
    .value_counts()
    .sort_index()
)


# ---------------------------------------------------------
# 12. Sample predictions
# ---------------------------------------------------------

print("\nFirst 10 predictions:")

print(
    final_predictions.head(10).to_string(
        index=False
    )
)


print("\nEvaluation note:")
print(
    "Threshold 0.40 was selected using validation data. "
    "The test set had previously been evaluated at threshold 0.30, "
    "so this 0.40 evaluation is reported transparently as a "
    "post-selection test evaluation rather than a pristine first-use holdout."
)