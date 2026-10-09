from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "SupplyPrescript Backend is running"


# --------------------------------------------------
# Shipment endpoints
# --------------------------------------------------

def test_get_shipments():
    response = client.get("/shipments")

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert any(shipment["shipment_id"] == "SHP001" for shipment in data)


def test_get_shipments_response_fields():
    response = client.get("/shipments")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    for shipment in data:
        assert "shipment_id" in shipment
        assert "origin" in shipment
        assert "destination" in shipment
        assert "planned_delivery_date" in shipment
        assert "actual_delivery_date" in shipment


def test_get_shipment():
    response = client.get("/shipments/SHP001")

    assert response.status_code == 200

    data = response.json()

    assert data["shipment_id"] == "SHP001"
    assert data["origin"] == "Bengaluru"
    assert data["destination"] == "Mumbai"


def test_get_shipment_response_fields():
    response = client.get("/shipments/SHP001")

    assert response.status_code == 200

    data = response.json()

    assert "shipment_id" in data
    assert "origin" in data
    assert "destination" in data
    assert "planned_delivery_date" in data
    assert "actual_delivery_date" in data


# --------------------------------------------------
# Prediction endpoints
# --------------------------------------------------

def test_get_prediction():
    response = client.get("/shipments/SHP001/prediction")

    assert response.status_code == 200

    data = response.json()

    assert data["shipment_id"] == "SHP001"
    assert data["delay_days"] == 2
    assert data["delay_label"] == "Delayed"
    assert data["delay_probability"] == 0.82
    assert data["risk_level"] == "High"


def test_prediction_response_fields():
    response = client.get("/shipments/SHP001/prediction")

    assert response.status_code == 200

    data = response.json()

    expected_fields = {
        "shipment_id",
        "delay_days",
        "delay_label",
        "delay_probability",
        "risk_level",
    }

    assert set(data.keys()) == expected_fields


def test_prediction_probability_range():
    response = client.get("/shipments/SHP001/prediction")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["delay_probability"], (int, float))
    assert 0 <= data["delay_probability"] <= 1


def test_prediction_values_have_expected_types():
    response = client.get("/shipments/SHP001/prediction")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["shipment_id"], str)
    assert isinstance(data["delay_days"], int)
    assert isinstance(data["delay_label"], str)
    assert isinstance(data["risk_level"], str)

    assert data["delay_label"] != ""
    assert data["risk_level"] != ""


# --------------------------------------------------
# Alternatives endpoint
# --------------------------------------------------

def test_get_alternatives():
    response = client.get("/shipments/SHP001/alternatives")

    assert response.status_code == 200

    data = response.json()

    assert data["order_id"] == "SHP001"
    assert data["recommended_action"] == "Alternate Supplier"
    assert data["estimated_cost"] is None
    assert "recommendation_reason" in data


def test_alternatives_response_fields():
    response = client.get("/shipments/SHP001/alternatives")

    assert response.status_code == 200

    data = response.json()

    expected_fields = {
        "alternative_id",
        "order_id",
        "recommended_action",
        "estimated_cost",
        "recommendation_reason",
    }

    assert set(data.keys()) == expected_fields


def test_alternatives_response_values():
    response = client.get("/shipments/SHP001/alternatives")

    assert response.status_code == 200

    data = response.json()

    assert data["alternative_id"] == "REC-SHP001"
    assert data["order_id"] == "SHP001"
    assert data["recommended_action"] == "Alternate Supplier"
    assert data["estimated_cost"] is None
    assert isinstance(data["recommendation_reason"], str)
    assert data["recommendation_reason"] != ""


def test_alternatives_recommendation_is_persisted():
    response = client.get("/shipments/SHP001/alternatives")

    assert response.status_code == 200

    data = response.json()

    assert data["alternative_id"] == "REC-SHP001"

    response_again = client.get("/shipments/SHP001/alternatives")

    assert response_again.status_code == 200

    data_again = response_again.json()

    assert data_again["alternative_id"] == "REC-SHP001"
    assert data_again["recommended_action"] == data["recommended_action"]


def test_alternatives_prediction_probability_out_of_range():
    from database import SessionLocal
    from models import Prediction

    db = SessionLocal()

    original_probability = None

    try:
        prediction = (
            db.query(Prediction)
            .filter(Prediction.shipment_id == "SHP001")
            .first()
        )

        assert prediction is not None

        original_probability = prediction.delay_probability

        prediction.delay_probability = 1.5
        db.commit()

        response = client.get("/shipments/SHP001/alternatives")

        assert response.status_code == 400
        assert response.json()["detail"] == (
            "prediction_probability must be between 0 and 1"
        )

    finally:
        if original_probability is not None:
            prediction.delay_probability = original_probability
            db.commit()

        db.close()


def test_alternatives_negative_probability():
    from database import SessionLocal
    from models import Prediction

    db = SessionLocal()

    original_probability = None

    try:
        prediction = (
            db.query(Prediction)
            .filter(Prediction.shipment_id == "SHP001")
            .first()
        )

        assert prediction is not None

        original_probability = prediction.delay_probability

        prediction.delay_probability = -0.1
        db.commit()

        response = client.get("/shipments/SHP001/alternatives")

        assert response.status_code == 400
        assert response.json()["detail"] == (
            "prediction_probability must be between 0 and 1"
        )

    finally:
        if original_probability is not None:
            prediction.delay_probability = original_probability
            db.commit()

        db.close()


# --------------------------------------------------
# Decision endpoints
# --------------------------------------------------

def test_save_decision():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "ALT001",
            "selected_action": "Use alternate carrier",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["shipment_id"] == "SHP001"
    assert data["alternative_id"] == "ALT001"
    assert data["selected_action"] == "Use alternate carrier"


def test_get_decisions():
    response = client.get("/shipments/SHP001/decisions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# --------------------------------------------------
# Not-found error tests
# --------------------------------------------------

def test_shipment_not_found():
    response = client.get("/shipments/SHP999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Shipment not found"


def test_another_shipment_not_found():
    response = client.get("/shipments/DOES_NOT_EXIST")

    assert response.status_code == 404
    assert response.json()["detail"] == "Shipment not found"


def test_prediction_not_found():
    response = client.get("/shipments/SHP999/prediction")

    assert response.status_code == 404
    assert response.json()["detail"] == "Prediction not found"


def test_alternatives_shipment_not_found():
    response = client.get("/shipments/SHP999/alternatives")

    assert response.status_code == 404
    assert response.json()["detail"] == "Shipment not found"


def test_decisions_shipment_not_found():
    response = client.get("/shipments/SHP999/decisions")

    assert response.status_code == 404
    assert response.json()["detail"] == "Shipment not found"


# --------------------------------------------------
# Decision input validation tests
# --------------------------------------------------

def test_empty_alternative_id():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "",
            "selected_action": "Use alternate carrier",
        },
    )

    assert response.status_code == 422


def test_empty_selected_action():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "ALT001",
            "selected_action": "",
        },
    )

    assert response.status_code == 422


def test_whitespace_only_alternative_id():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "   ",
            "selected_action": "Use alternate carrier",
        },
    )

    assert response.status_code == 422


def test_whitespace_only_selected_action():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "ALT001",
            "selected_action": "   ",
        },
    )

    assert response.status_code == 422


def test_selected_action_does_not_match_alternative():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "ALT001",
            "selected_action": "Wrong action",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Selected action does not match the alternative"
    )


def test_alternative_not_found():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "ALT999",
            "selected_action": "Some action",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Alternative not found for this shipment"
    )


# --------------------------------------------------
# Day 6: Decision retrieval tests
# --------------------------------------------------

def test_decisions_response_fields():
    response = client.get("/shipments/SHP001/decisions")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        expected_fields = {
            "decision_id",
            "shipment_id",
            "alternative_id",
            "selected_action",
            "decision_timestamp",
        }

        assert set(data[0].keys()) == expected_fields


def test_multiple_decisions_can_be_saved_and_retrieved():
    from database import SessionLocal
    from models import Shipment, Alternative

    shipment_id = "TEST-DAY6"
    alternative_data = [
        ("TEST-DAY6-ALT1", "Use alternate carrier"),
        ("TEST-DAY6-ALT2", "Continue with current carrier"),
    ]

    db = SessionLocal()

    try:
        shipment = (
            db.query(Shipment)
            .filter(Shipment.shipment_id == shipment_id)
            .first()
        )

        if shipment is None:
            shipment = Shipment(
                shipment_id=shipment_id,
                origin="Bengaluru",
                destination="Chennai",
            )
            db.add(shipment)
            db.flush()

        for alternative_id, action in alternative_data:
            alternative = (
                db.query(Alternative)
                .filter(Alternative.alternative_id == alternative_id)
                .first()
            )

            if alternative is None:
                db.add(
                    Alternative(
                        alternative_id=alternative_id,
                        shipment_id=shipment_id,
                        action=action,
                    )
                )

        db.commit()

    finally:
        db.close()

    # Retrieve existing test decisions so repeated test runs
    # don't fail because the database already contains records.
    existing_response = client.get(
        f"/shipments/{shipment_id}/decisions"
    )

    assert existing_response.status_code == 200

    existing_actions = {
        decision["selected_action"]
        for decision in existing_response.json()
    }

    for alternative_id, action in alternative_data:
        if action not in existing_actions:
            save_response = client.post(
                f"/shipments/{shipment_id}/decisions",
                json={
                    "alternative_id": alternative_id,
                    "selected_action": action,
                },
            )

            assert save_response.status_code == 200

    response = client.get(
        f"/shipments/{shipment_id}/decisions"
    )

    assert response.status_code == 200

    decisions = response.json()

    saved_actions = {
        decision["selected_action"]
        for decision in decisions
    }

    assert {
        "Use alternate carrier",
        "Continue with current carrier",
    }.issubset(saved_actions)


def test_retrieved_decisions_have_valid_values():
    response = client.get("/shipments/SHP001/decisions")

    assert response.status_code == 200

    decisions = response.json()

    for decision in decisions:
        assert isinstance(decision["decision_id"], int)
        assert decision["shipment_id"] == "SHP001"
        assert isinstance(decision["alternative_id"], str)
        assert isinstance(decision["selected_action"], str)
        assert isinstance(decision["decision_timestamp"], str)


def test_decisions_are_associated_with_requested_shipment():
    response = client.get("/shipments/SHP001/decisions")

    assert response.status_code == 200

    decisions = response.json()

    for decision in decisions:
        assert decision["shipment_id"] == "SHP001"


def test_shipment_without_decisions_returns_empty_list():
    from database import SessionLocal
    from models import Shipment

    shipment_id = "TEST-DAY6-EMPTY"

    db = SessionLocal()

    try:
        shipment = (
            db.query(Shipment)
            .filter(Shipment.shipment_id == shipment_id)
            .first()
        )

        if shipment is None:
            db.add(
                Shipment(
                    shipment_id=shipment_id,
                    origin="Pune",
                    destination="Hyderabad",
                )
            )
            db.commit()

    finally:
        db.close()

    response = client.get(
        f"/shipments/{shipment_id}/decisions"
    )

    assert response.status_code == 200
    assert response.json() == []