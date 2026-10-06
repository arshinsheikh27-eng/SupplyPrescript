import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ---------------------------------------------------------
# 1. Load prepared order-level dataset
# ---------------------------------------------------------

DATA_PATH = "data/processed/supplyprescript_order_model_data.csv"

df = pd.read_csv(DATA_PATH)

df["order_date"] = pd.to_datetime(df["order_date"])

# Keep chronological order
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
# 3. Chronological train / validation / test split
# ---------------------------------------------------------

test_split = int(len(df) * 0.80)

X_train_full = X.iloc[:test_split]
y_train_full = y.iloc[:test_split]

X_test = X.iloc[test_split:]
y_test = y.iloc[test_split:]


validation_split = int(len(X_train_full) * 0.80)

X_train = X_train_full.iloc[:validation_split]
y_train = y_train_full.iloc[:validation_split]

X_validation = X_train_full.iloc[validation_split:]
y_validation = y_train_full.iloc[validation_split:]


print("Dataset split:")
print("Training:", len(X_train))
print("Validation:", len(X_validation))
print("Test:", len(X_test))


# ---------------------------------------------------------
# 4. Preprocessing
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
            OneHotEncoder(handle_unknown="ignore")
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
# 5. Logistic Regression baseline
# ---------------------------------------------------------

logistic_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            LogisticRegression(max_iter=1000)
        )
    ]
)


# ---------------------------------------------------------
# 6. Random Forest model
# ---------------------------------------------------------

random_forest_model = Pipeline(
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
# 7. Train both models
# ---------------------------------------------------------

print("\nTraining Logistic Regression...")
logistic_model.fit(X_train, y_train)

print("Training Random Forest...")
random_forest_model.fit(X_train, y_train)


# ---------------------------------------------------------
# 8. Evaluate models on validation data
# ---------------------------------------------------------

models = {
    "Logistic Regression": logistic_model,
    "Random Forest": random_forest_model
}

results = []

for name, model in models.items():

    probability = model.predict_proba(X_validation)[:, 1]

    prediction = (probability >= 0.50).astype(int)

    results.append(
        {
            "model": name,
            "accuracy": accuracy_score(
                y_validation,
                prediction
            ),
            "precision": precision_score(
                y_validation,
                prediction,
                zero_division=0
            ),
            "recall": recall_score(
                y_validation,
                prediction,
                zero_division=0
            ),
            "f1": f1_score(
                y_validation,
                prediction,
                zero_division=0
            ),
            "roc_auc": roc_auc_score(
                y_validation,
                probability
            )
        }
    )


# ---------------------------------------------------------
# 9. Display comparison
# ---------------------------------------------------------

results_df = pd.DataFrame(results)

print("\nValidation Model Comparison:")
print(
    results_df.to_string(index=False)
)