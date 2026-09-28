from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Shipment, Prediction, Alternative, Decision


app = FastAPI(
    title="SupplyPrescript Backend API",
    description="Backend API for shipment delay prediction and decision support",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DecisionRequest(BaseModel):
    alternative_id: str
    selected_action: str


@app.get("/")
def home():
    return {
        "message": "SupplyPrescript Backend is running"
    }


@app.get("/shipments")
def get_shipments(db: Session = Depends(get_db)):
    shipments = db.query(Shipment).all()

    return [
        {
            "shipment_id": shipment.shipment_id,
            "origin": shipment.origin,
            "destination": shipment.destination,
            "planned_delivery_date": shipment.planned_delivery_date,
            "actual_delivery_date": shipment.actual_delivery_date,
        }
        for shipment in shipments
    ]


@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: str, db: Session = Depends(get_db)):
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == shipment_id)
        .first()
    )

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    return {
        "shipment_id": shipment.shipment_id,
        "origin": shipment.origin,
        "destination": shipment.destination,
        "planned_delivery_date": shipment.planned_delivery_date,
        "actual_delivery_date": shipment.actual_delivery_date,
    }


@app.get("/shipments/{shipment_id}/prediction")
def get_prediction(shipment_id: str, db: Session = Depends(get_db)):
    prediction = (
        db.query(Prediction)
        .filter(Prediction.shipment_id == shipment_id)
        .first()
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    return {
        "shipment_id": prediction.shipment_id,
        "delay_days": prediction.delay_days,
        "delay_label": prediction.delay_label,
        "delay_probability": prediction.delay_probability,
        "risk_level": prediction.risk_level,
    }


@app.get("/shipments/{shipment_id}/alternatives")
def get_alternatives(shipment_id: str, db: Session = Depends(get_db)):
    alternatives = (
        db.query(Alternative)
        .filter(Alternative.shipment_id == shipment_id)
        .all()
    )

    if not alternatives:
        raise HTTPException(
            status_code=404,
            detail="No alternatives found"
        )

    return [
        {
            "alternative_id": alternative.alternative_id,
            "shipment_id": alternative.shipment_id,
            "estimated_cost": alternative.estimated_cost,
            "estimated_time": alternative.estimated_time,
            "action": alternative.action,
        }
        for alternative in alternatives
    ]


@app.post("/shipments/{shipment_id}/decisions")
def save_decision(
    shipment_id: str,
    decision_request: DecisionRequest,
    db: Session = Depends(get_db)
):
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == shipment_id)
        .first()
    )

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    alternative = (
        db.query(Alternative)
        .filter(
            Alternative.alternative_id == decision_request.alternative_id,
            Alternative.shipment_id == shipment_id
        )
        .first()
    )

    if alternative is None:
        raise HTTPException(
            status_code=404,
            detail="Alternative not found for this shipment"
        )

    decision = Decision(
        shipment_id=shipment_id,
        alternative_id=decision_request.alternative_id,
        selected_action=decision_request.selected_action,
        decision_timestamp=datetime.now()
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return {
        "decision_id": decision.decision_id,
        "shipment_id": decision.shipment_id,
        "alternative_id": decision.alternative_id,
        "selected_action": decision.selected_action,
        "decision_timestamp": decision.decision_timestamp,
    }


@app.get("/shipments/{shipment_id}/decisions")
def get_decisions(shipment_id: str, db: Session = Depends(get_db)):
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == shipment_id)
        .first()
    )

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    decisions = (
        db.query(Decision)
        .filter(Decision.shipment_id == shipment_id)
        .all()
    )

    return [
        {
            "decision_id": decision.decision_id,
            "shipment_id": decision.shipment_id,
            "alternative_id": decision.alternative_id,
            "selected_action": decision.selected_action,
            "decision_timestamp": decision.decision_timestamp,
        }
        for decision in decisions
    ]