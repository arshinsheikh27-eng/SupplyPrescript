from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "SupplyPrescript Backend is running"


def test_get_shipments():
    response = client.get("/shipments")

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["shipment_id"] == "SHP001"


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


def test_get_prediction():
    response = client.get("/shipments/SHP001/prediction")

    assert response.status_code == 200

    data = response.json()

    assert data["shipment_id"] == "SHP001"
    assert data["delay_days"] == 2
    assert data["delay_label"] == "Delayed"
    assert data["delay_probability"] == 0.82
    assert data["risk_level"] == "High"


def test_get_alternatives():
    response = client.get("/shipments/SHP001/alternatives")

    assert response.status_code == 200

    data = response.json()

    assert data["order_id"] == "SHP001"
    assert data["recommended_action"] == "Alternate Supplier"
    assert data["estimated_cost"] is None
    assert "recommendation_reason" in data


def test_save_decision():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "ALT001",
            "selected_action": "Use alternate carrier"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["shipment_id"] == "SHP001"
    assert data["alternative_id"] == "ALT001"
    assert data["selected_action"] == "Use alternate carrier"


def test_get_decisions():
    response = client.get("/shipments/SHP001/decisions")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


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


def test_empty_alternative_id():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "",
            "selected_action": "Use alternate carrier"
        }
    )

    assert response.status_code == 422


def test_empty_selected_action():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "ALT001",
            "selected_action": ""
        }
    )

    assert response.status_code == 422


def test_whitespace_only_alternative_id():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "   ",
            "selected_action": "Use alternate carrier"
        }
    )

    assert response.status_code == 422


def test_whitespace_only_selected_action():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "ALT001",
            "selected_action": "   "
        }
    )

    assert response.status_code == 422


def test_selected_action_does_not_match_alternative():
    response = client.post(
        "/shipments/SHP001/decisions",
        json={
            "alternative_id": "ALT001",
            "selected_action": "Wrong action"
        }
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
            "selected_action": "Some action"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Alternative not found for this shipment"
    )