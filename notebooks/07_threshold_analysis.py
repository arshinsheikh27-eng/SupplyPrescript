import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# Load baseline test predictions
df = pd.read_csv(
    "data/processed/baseline_test_predictions.csv"
)

actual = df["late_delivery_risk"]
probability = df["predicted_probability"]

# Thresholds to compare
thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]

results = []

for threshold in thresholds:

    predicted = (probability >= threshold).astype(int)

    results.append({
        "threshold": threshold,
        "accuracy": accuracy_score(actual, predicted),
        "precision": precision_score(actual, predicted, zero_division=0),
        "recall": recall_score(actual, predicted, zero_division=0),
        "f1": f1_score(actual, predicted, zero_division=0)
    })

results_df = pd.DataFrame(results)

print("\nThreshold Comparison:")
print(results_df.to_string(index=False))