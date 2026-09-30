# SupplyPrescript Optimization Module

def recommend_action(order_id, late_delivery_risk, prediction_probability):

    if late_delivery_risk == 0:
        action = "No Action"
        cost = 0
        reason = "Low delay risk"

    elif prediction_probability <= 0.75:
        action = "Monitor Shipment"
        cost = 500
        reason = "Moderate delay risk"

    elif prediction_probability <= 0.90:
        action = "Alternate Supplier"
        cost = 10000
        reason = "High delay risk"

    else:
        action = "Air Freight"
        cost = 15000
        reason = "Critical delay risk"

    return {
        "order_id": order_id,
        "recommended_action": action,
        "estimated_cost": cost,
        "recommendation_reason": reason
    }


# Sample Test Data

orders = [
    (50101, 0, 0.18),
    (50102, 1, 0.83),
    (50103, 0, 0.42),
    (50104, 1, 0.71),
    (50105, 1, 0.92)
]

for order in orders:
    result = recommend_action(
        order[0],
        order[1],
        order[2]
    )

    print(result)

