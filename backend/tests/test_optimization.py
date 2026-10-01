from optimization.optimization_model import generate_recommendation


def test_no_risk():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=0,
        prediction_probability=0.20
    )

    assert result["order_id"] == "SHP001"
    assert result["recommended_action"] == "No Action"


def test_monitor_shipment():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.60
    )

    assert result["recommended_action"] == "Monitor Shipment"


def test_alternate_supplier():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.82
    )

    assert result["recommended_action"] == "Alternate Supplier"


def test_air_freight():
    result = generate_recommendation(
        order_id="SHP001",
        late_delivery_risk=1,
        prediction_probability=0.95
    )

    assert result["recommended_action"] == "Air Freight"


def test_invalid_risk_value():
    try:
        generate_recommendation(
            order_id="SHP001",
            late_delivery_risk=2,
            prediction_probability=0.82
        )
        assert False
    except ValueError:
        assert True


def test_invalid_probability():
    try:
        generate_recommendation(
            order_id="SHP001",
            late_delivery_risk=1,
            prediction_probability=1.5
        )
        assert False
    except ValueError:
        assert True