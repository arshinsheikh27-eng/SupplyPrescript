import pandas as pd
from sklearn.metrics import confusion_matrix

# Load baseline predictions
predictions = pd.read_csv(
    "data/processed/baseline_test_predictions.csv"
)

# Create error type
predictions["error_type"] = "Correct"

predictions.loc[
    (predictions["late_delivery_risk"] == 0) &
    (predictions["predicted_risk"] == 1),
    "error_type"
] = "False Positive"

predictions.loc[
    (predictions["late_delivery_risk"] == 1) &
    (predictions["predicted_risk"] == 0),
    "error_type"
] = "False Negative"

# Display confusion matrix
cm = confusion_matrix(
    predictions["late_delivery_risk"],
    predictions["predicted_risk"]
)

print("Confusion Matrix:")
print(cm)

# Error summary
print("\nError Type Counts:")
print(predictions["error_type"].value_counts())

# False positives
false_positives = predictions[
    predictions["error_type"] == "False Positive"
]

# False negatives
false_negatives = predictions[
    predictions["error_type"] == "False Negative"
]

print("\nFalse Positives:", len(false_positives))
print("False Negatives:", len(false_negatives))

# Show examples
print("\nSample False Positives:")
print(false_positives.head(10).to_string(index=False))

print("\nSample False Negatives:")
print(false_negatives.head(10).to_string(index=False))