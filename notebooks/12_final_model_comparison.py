import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


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

X = df[FEATURES]
y = df[TARGET]


# ---------------------------------------------------------
# 2. Chronological train / validation / test split
# ---------------------------------------------------------

train_full_size = int(len(df) * 0.80)

train_full = df.iloc[:train_full_size]
test = df.iloc[train_full_size:]

train_size = int(len(train_full) * 0.80)

train = train_full.iloc[:train_size]
validation = train_full.iloc[train_size:]


X_train = train[FEATURES]
y_train = train[TARGET]

X_validation = validation[FEATURES]
y_validation = validation[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]


print("Dataset split:")
print(f"Training   : {len(train)}")
print(f"Validation : {len(validation)}")
print(f"Test       : {len(test)}")

print("\nDate ranges:")
print(
    "Training   :",
    train["order_date"].min(),
    "to",
    train["order_date"].max()
)
print(
    "Validation :",
    validation["order_date"].min(),
    "to",
    validation["order_date"].max()
)
print(
    "Test       :",
    test["order_date"].min(),
    "to",
    test["order_date"].max()
)


# ---------------------------------------------------------
# 3. Preprocessing for Logistic Regression
# ---------------------------------------------------------

logistic_preprocessor = ColumnTransformer([
    (
        "numeric",
        Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
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
# 4. Preprocessing for Random Forest
# ---------------------------------------------------------

rf_preprocessor = ColumnTransformer([
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
# 5. Define models
# ---------------------------------------------------------

logistic_model = Pipeline([
    (
        "preprocessor",
        logistic_preprocessor
    ),
    (
        "model",
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    ),
])


random_forest_model = Pipeline([
    (
        "preprocessor",
        rf_preprocessor
    ),
    (
        "model",
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
# 6. Evaluation function
# ---------------------------------------------------------

def evaluate_model(name, model):

    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_validation)
    probabilities = model.predict_proba(X_validation)[:, 1]

    results = {
        "Model": name,
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
        "ROC-AUC": roc_auc_score(
            y_validation,
            probabilities
        ),
    }

    return results


# ---------------------------------------------------------
# 7. Compare models
# ---------------------------------------------------------

results = []

results.append(
    evaluate_model(
        "Logistic Regression",
        logistic_model
    )
)

results.append(
    evaluate_model(
        "Random Forest",
        random_forest_model
    )
)


# ---------------------------------------------------------
# 8. Display comparison
# ---------------------------------------------------------

comparison = pd.DataFrame(results)

print("\n" + "=" * 75)
print("FINAL MODEL COMPARISON - VALIDATION SET")
print("=" * 75)

print(
    comparison.to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}"
    )
)


# ---------------------------------------------------------
# 9. Show metric differences
# ---------------------------------------------------------

lr = comparison[
    comparison["Model"] == "Logistic Regression"
].iloc[0]

rf = comparison[
    comparison["Model"] == "Random Forest"
].iloc[0]

print("\nMetric Differences (Random Forest - Logistic Regression):")

for metric in [
    "Accuracy",
    "Precision",
    "Recall",
    "F1",
    "ROC-AUC",
]:
    difference = rf[metric] - lr[metric]
    print(f"{metric:10s}: {difference:+.6f}")


print("\nNote:")
print(
    "The validation set is used for model comparison. "
    "The final test set remains untouched until the final pipeline is frozen."
)