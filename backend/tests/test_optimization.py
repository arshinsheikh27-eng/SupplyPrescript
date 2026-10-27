import pytest

from optimization.optimization_model import generate_recommendation


# --------------------------------------------------
# BASIC RECOMMENDATION TESTS
# --------------------------------------------------

def test_no_risk():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=0,
        prediction_probability=0.20,
    )

    assert result["order_id"] == "SHP001"
    assert result["recommended_action"] == "No Action"


def test_monitor_shipment():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.60,
    )

    assert result["recommended_action"] == "Monitor Shipment"


def test_alternate_supplier():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.82,
    )

    assert result["recommended_action"] == "Alternate Supplier"


def test_air_freight():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.95,
    )

    assert result["recommended_action"] == "Air Freight"


# --------------------------------------------------
# PROBABILITY BOUNDARY TESTS
# --------------------------------------------------

def test_probability_zero_with_risk():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.0,
    )

    assert result["recommended_action"] == "No Action"


def test_probability_exactly_050():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.50,
    )

    assert result["recommended_action"] == "Monitor Shipment"


def test_probability_exactly_075():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.75,
    )

    assert result["recommended_action"] == "Monitor Shipment"


def test_probability_just_above_075():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.751,
    )

    assert result["recommended_action"] == "Alternate Supplier"


def test_probability_exactly_090():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.90,
    )

    assert result["recommended_action"] == "Alternate Supplier"


def test_probability_just_above_090():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.901,
    )

    assert result["recommended_action"] == "Air Freight"


def test_probability_one():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=1.0,
    )

    assert result["recommended_action"] == "Air Freight"


def test_probability_below_monitor_threshold():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.49,
    )

    assert result["recommended_action"] == "No Action"


# --------------------------------------------------
# INVALID INPUT TESTS
# --------------------------------------------------

def test_invalid_risk_value():
    with pytest.raises(
        ValueError,
        match="late_delivery_risk must be 0 or 1",
    ):
        generate_recommendation(
            order_id="SHP001",
            late_delivery_risk=2,
            prediction_probability=0.82,
        )


@pytest.mark.parametrize("probability", [-0.01, 1.01])
def test_invalid_probability(probability):
    with pytest.raises(
        ValueError,
        match="prediction_probability must be between 0 and 1",
    ):
        generate_recommendation(
            order_id="SHP001",
            late_delivery_risk=1,
            prediction_probability=probability,
        )


# --------------------------------------------------
# RECOMMENDATION OUTPUT TESTS
# --------------------------------------------------

def test_recommendation_output_fields():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.82,
    )

    assert set(result.keys()) == {
        "order_id",
        "recommended_action",
        "estimated_cost",
        "recommendation_reason",
    }


def test_recommendation_output_values():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.82,
    )

    assert result["order_id"] == "SHP001"
    assert result["recommended_action"] == "Alternate Supplier"
    assert result["estimated_cost"] is None
    assert isinstance(result["recommendation_reason"], str)
    assert result["recommendation_reason"] != ""