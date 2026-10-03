from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

project_folder = Path(__file__).resolve().parent.parent
input_path = (
    project_folder
    / "data"
    / "processed"
    / "supplyprescript_order_model_data.csv"
)

df = pd.read_csv(input_path, parse_dates=["order_date"])
df = df.sort_values("order_date").reset_index(drop=True)

target = "late_delivery_risk"
id_column = "Order Id"
date_column = "order_date"

categorical_features = [
    "shipping_mode",
    "payment_type",
    "market",
    "order_region",
    "customer_segment",
]

numeric_features = [
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

features = categorical_features + numeric_features

# Chronological 80/20 split: earlier orders train; later orders test.
split_index = int(len(df) * 0.8)
train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()

X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

print("========== TIME SPLIT ==========")
print("Train rows:", len(train))
print("Test rows:", len(test))
print("Train date range:", train[date_column].min(), "to", train[date_column].max())
print("Test date range:", test[date_column].min(), "to", test[date_column].max())
print("Train target rate:", round(y_train.mean(), 4))
print("Test target rate:", round(y_test.mean(), 4))

# Preprocessing: impute numeric missing values and scale them;
# one-hot encode categorical variables, ignoring unseen test categories.
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features),
])

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000)),
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("\n========== TEST METRICS ==========")
print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
print("Precision:", round(precision_score(y_test, predictions, zero_division=0), 4))
print("Recall:", round(recall_score(y_test, predictions, zero_division=0), 4))
print("F1:", round(f1_score(y_test, predictions, zero_division=0), 4))
print("ROC-AUC:", round(roc_auc_score(y_test, probabilities), 4))

print("\n========== CONFUSION MATRIX ==========")
print(confusion_matrix(y_test, predictions))

print("\n========== CLASSIFICATION REPORT ==========")
print(classification_report(y_test, predictions, zero_division=0))

# Save test predictions for later error review; keep this generated file local.
results = test[[id_column, date_column, target]].copy()
results["predicted_risk"] = predictions
results["predicted_probability"] = probabilities

output_path = (
    project_folder
    / "data"
    / "processed"
    / "baseline_test_predictions.csv"
)
results.to_csv(output_path, index=False)
print("\nSaved test predictions to:", output_path)