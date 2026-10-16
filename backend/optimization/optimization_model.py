from typing import TypedDict


class RecommendationResult(TypedDict):
    """Structure returned by the recommendation engine."""

    order_id: str
    recommended_action: str
    estimated_cost: None
    recommendation_reason: str


def generate_recommendation(
    order_id: str,
    late_delivery_risk: int,
    prediction_probability: float,
) -> RecommendationResult:
    """
    Generate a V1 shipment recommendation using the team's
    confirmed optimization rules.

    Args:
        order_id: Identifier of the shipment or order.
        late_delivery_risk: Risk indicator; must be 0 or 1.
        prediction_probability: Probability between 0 and 1.

    Returns:
        A recommendation dictionary containing the order ID,
        recommended action, estimated cost, and explanation.

    Raises:
        ValueError: If the risk indicator or probability is invalid.
    """

    if late_delivery_risk not in (0, 1):
        raise ValueError("late_delivery_risk must be 0 or 1")

    if not 0 <= prediction_probability <= 1:
        raise ValueError(
            "prediction_probability must be between 0 and 1"
        )

    if late_delivery_risk == 0:
        recommended_action = "No Action"
        recommendation_reason = (
            "Shipment has no late delivery risk."
        )

    elif 0.50 <= prediction_probability <= 0.75:
        recommended_action = "Monitor Shipment"
        recommendation_reason = (
            "Shipment has delivery risk with a moderate "
            "prediction probability."
        )

    elif 0.75 < prediction_probability <= 0.90:
        recommended_action = "Alternate Supplier"
        recommendation_reason = (
            "Shipment has delivery risk with a high "
            "prediction probability."
        )

    elif prediction_probability > 0.90:
        recommended_action = "Air Freight"
        recommendation_reason = (
            "Shipment has delivery risk with a very high "
            "prediction probability."
        )

    else:
        recommended_action = "No Action"
        recommendation_reason = (
            "Prediction probability is below the defined "
            "V1 risk thresholds."
        )

    return {
        "order_id": order_id,
        "recommended_action": recommended_action,
        "estimated_cost": None,
        "recommendation_reason": recommendation_reason,
    }