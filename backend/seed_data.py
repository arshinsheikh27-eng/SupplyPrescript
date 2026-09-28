from datetime import date, datetime

from database import SessionLocal
from models import Shipment, Prediction, Alternative


db = SessionLocal()

shipment = Shipment(
    shipment_id="SHP001",
    origin="Bengaluru",
    destination="Mumbai",
    planned_delivery_date=date(2026, 9, 30),
    actual_delivery_date=None,
)

prediction = Prediction(
    prediction_id=1,
    shipment_id="SHP001",
    delay_days=2,
    delay_label="Delayed",
    delay_probability=0.82,
    risk_level="High",
)

alternative1 = Alternative(
    alternative_id="ALT001",
    shipment_id="SHP001",
    estimated_cost=1500.0,
    estimated_time=1.0,
    action="Use alternate carrier",
)

alternative2 = Alternative(
    alternative_id="ALT002",
    shipment_id="SHP001",
    estimated_cost=800.0,
    estimated_time=2.0,
    action="Continue with current carrier",
)

db.add(shipment)
db.add(prediction)
db.add(alternative1)
db.add(alternative2)

db.commit()
db.close()

print("Sample shipment data inserted successfully")