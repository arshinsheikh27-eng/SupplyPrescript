from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Shipment, Prediction, Alternative, Decision
from schemas import (
    ShipmentResponse,
    PredictionResponse,
    AlternativeResponse,
    DecisionResponse,
    DecisionRequestSchema,
)
from optimization.optimization_model import generate_recommendation


app = FastAPI(
    title="SupplyPrescript Backend API",
    description=(
        "Backend API for shipment delay prediction "
        "and decision support"
    ),
    version="1.0.0",
)


# --------------------------------------------------
# Database dependency
# --------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "SupplyPrescript Backend is running"
    }


# --------------------------------------------------
# Shipment endpoints
# --------------------------------------------------

@app.get(
    "/shipments",
    response_model=list[ShipmentResponse],
)
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


@app.get(
    "/shipments/{shipment_id}",
    response_model=ShipmentResponse,
)
def get_shipment(
    shipment_id: str,
    db: Session = Depends(get_db),
):
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == shipment_id)
        .first()
    )

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    return {
        "shipment_id": shipment.shipment_id,
        "origin": shipment.origin,
        "destination": shipment.destination,
        "planned_delivery_date": shipment.planned_delivery_date,
        "actual_delivery_date": shipment.actual_delivery_date,
    }


# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------

@app.get(
    "/shipments/{shipment_id}/prediction",
    response_model=PredictionResponse,
)
def get_prediction(
    shipment_id: str,
    db: Session = Depends(get_db),
):
    # Preserve the existing API behavior:
    # return "Prediction not found" when no prediction exists.
    prediction = (
        db.query(Prediction)
        .filter(Prediction.shipment_id == shipment_id)
        .first()
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found",
        )

    return {
        "shipment_id": prediction.shipment_id,
        "delay_days": prediction.delay_days,
        "delay_label": prediction.delay_label,
        "delay_probability": prediction.delay_probability,
        "risk_level": prediction.risk_level,
    }


# --------------------------------------------------
# Alternatives and recommendation endpoint
# --------------------------------------------------

@app.get(
    "/shipments/{shipment_id}/alternatives",
    response_model=AlternativeResponse,
)
def get_alternatives(
    shipment_id: str,
    db: Session = Depends(get_db),
):
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == shipment_id)
        .first()
    )

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    prediction = (
        db.query(Prediction)
        .filter(Prediction.shipment_id == shipment_id)
        .first()
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found",
        )

    if prediction.delay_probability is None:
        raise HTTPException(
            status_code=400,
            detail="Prediction probability is missing",
        )

    # V1 risk mapping.
    if prediction.risk_level == "No Risk":
        late_delivery_risk = 0
    else:
        late_delivery_risk = 1

    try:
        recommendation = generate_recommendation(
            order_id=shipment.shipment_id,
            late_delivery_risk=late_delivery_risk,
            prediction_probability=prediction.delay_probability,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    # Store the generated recommendation using a stable ID.
    alternative_id = f"REC-{shipment_id}"

    alternative = (
        db.query(Alternative)
        .filter(Alternative.alternative_id == alternative_id)
        .first()
    )

    if alternative is None:
        alternative = Alternative(
            alternative_id=alternative_id,
            shipment_id=shipment_id,
            estimated_cost=recommendation["estimated_cost"],
            estimated_time=None,
            action=recommendation["recommended_action"],
            recommendation_reason=recommendation[
                "recommendation_reason"
            ],
        )

        db.add(alternative)
    else:
        alternative.estimated_cost = recommendation["estimated_cost"]
        alternative.action = recommendation["recommended_action"]
        alternative.recommendation_reason = recommendation[
            "recommendation_reason"
        ]

    db.commit()
    db.refresh(alternative)

    return {
        "alternative_id": alternative.alternative_id,
        "order_id": recommendation["order_id"],
        "recommended_action": recommendation["recommended_action"],
        "estimated_cost": recommendation["estimated_cost"],
        "recommendation_reason": recommendation[
            "recommendation_reason"
        ],
    }


# --------------------------------------------------
# Save decision endpoint
# --------------------------------------------------

@app.post(
    "/shipments/{shipment_id}/decisions",
    response_model=DecisionResponse,
)
def save_decision(
    shipment_id: str,
    decision_request: DecisionRequestSchema,
    db: Session = Depends(get_db),
):
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == shipment_id)
        .first()
    )

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    alternative = (
        db.query(Alternative)
        .filter(
            Alternative.alternative_id
            == decision_request.alternative_id,
            Alternative.shipment_id == shipment_id,
        )
        .first()
    )

    if alternative is None:
        raise HTTPException(
            status_code=404,
            detail="Alternative not found for this shipment",
        )

    if alternative.action != decision_request.selected_action:
        raise HTTPException(
            status_code=400,
            detail="Selected action does not match the alternative",
        )

    decision = Decision(
        shipment_id=shipment_id,
        alternative_id=decision_request.alternative_id,
        selected_action=decision_request.selected_action,
        decision_timestamp=datetime.now(),
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


# --------------------------------------------------
# Retrieve decisions endpoint
# --------------------------------------------------

@app.get(
    "/shipments/{shipment_id}/decisions",
    response_model=list[DecisionResponse],
)
def get_decisions(
    shipment_id: str,
    db: Session = Depends(get_db),
):
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == shipment_id)
        .first()
    )

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
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