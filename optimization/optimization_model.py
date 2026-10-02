import pandas as pd

def recommend_action(order_id, late_delivery_risk, prediction_probability):

    if late_delivery_risk == 1 and prediction_probability > 0.90:
        return {
            "order_id": order_id,
            "recommended_action": "Air Freight",
            "estimated_cost": 15000,
            "recommendation_reason": "Critical delay risk"
        }

    elif late_delivery_risk == 1 and prediction_probability > 0.70:
        return {
            "order_id": order_id,
            "recommended_action": "Alternate Supplier",
            "estimated_cost": 10000,
            "recommendation_reason": "High delay risk"
        }

    elif late_delivery_risk == 1 and prediction_probability > 0.40:
        return {
            "order_id": order_id,
            "recommended_action": "Monitor Shipment",
            "estimated_cost": 500,
            "recommendation_reason": "Moderate delay risk"
        }

    else:
        return {
            "order_id": order_id,
            "recommended_action": "No Action",
            "estimated_cost": 0,
            "recommendation_reason": "Low delay risk"
        }


df = pd.read_csv("data/final_test_predictions_threshold_040.csv")

results = []

for _, row in df.iterrows():

    result = recommend_action(
        row["Order Id"],
        row["predicted_risk"],
        row["predicted_probability"]
    )

    results.append(result)

results_df = pd.DataFrame(results)

print(results_df.head())

results_df.to_csv(
    "data/optimization_results.csv",
    index=False
)

print("\nOptimization completed successfully!")
print("Results saved to data/optimization_results.csv")
print("Total Orders Processed:", len(results_df))