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


def test_get_shipment():
    response = client.get("/shipments/SHP001")

    assert response.status_code == 200

    data = response.json()

    assert data["shipment_id"] == "SHP001"
    assert data["origin"] == "Bengaluru"
    assert data["destination"] == "Mumbai"


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