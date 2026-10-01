from datetime import date

from database import SessionLocal
from models import Shipment, Prediction, Alternative


db = SessionLocal()

try:
    # -----------------------------
    # Shipment
    # -----------------------------
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == "SHP001")
        .first()
    )

    if shipment is None:
        shipment = Shipment(
            shipment_id="SHP001",
            origin="Bengaluru",
            destination="Mumbai",
            planned_delivery_date=date(2026, 9, 30),
            actual_delivery_date=None,
        )
        db.add(shipment)
        print("Added shipment SHP001")
    else:
        print("Shipment SHP001 already exists")

    # -----------------------------
    # Prediction
    # -----------------------------
    prediction = (
        db.query(Prediction)
        .filter(Prediction.prediction_id == 1)
        .first()
    )

    if prediction is None:
        prediction = Prediction(
            prediction_id=1,
            shipment_id="SHP001",
            delay_days=2,
            delay_label="Delayed",
            delay_probability=0.82,
            risk_level="High",
        )
        db.add(prediction)
        print("Added prediction for SHP001")
    else:
        print("Prediction already exists")

    # -----------------------------
    # Alternative ALT001
    # -----------------------------
    alternative1 = (
        db.query(Alternative)
        .filter(Alternative.alternative_id == "ALT001")
        .first()
    )

    if alternative1 is None:
        alternative1 = Alternative(
            alternative_id="ALT001",
            shipment_id="SHP001",
            estimated_cost=1500.0,
            estimated_time=1.0,
            action="Use alternate carrier",
        )
        db.add(alternative1)
        print("Added alternative ALT001")
    else:
        print("Alternative ALT001 already exists")

    # -----------------------------
    # Alternative ALT002
    # -----------------------------
    alternative2 = (
        db.query(Alternative)
        .filter(Alternative.alternative_id == "ALT002")
        .first()
    )

    if alternative2 is None:
        alternative2 = Alternative(
            alternative_id="ALT002",
            shipment_id="SHP001",
            estimated_cost=800.0,
            estimated_time=2.0,
            action="Continue with current carrier",
        )
        db.add(alternative2)
        print("Added alternative ALT002")
    else:
        print("Alternative ALT002 already exists")

    db.commit()

    print("Seed data check completed successfully")

finally:
    db.close()