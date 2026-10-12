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


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="SupplyPrescript Backend API",
    description=(
        "Backend API for shipment delay prediction and decision support. "
        "The API provides shipment details, prediction results, "
        "recommendations, and persistent decision history."
    ),
    version="1.0.0",
)


# --------------------------------------------------
# DATABASE SESSION
# --------------------------------------------------

def get_db():
    """Create and close a database session for each request."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get(
    "/",
    summary="Check backend status",
    description="Returns a message confirming that the backend is running.",
    tags=["Health"],
)
def home():
    return {"message": "SupplyPrescript Backend is running"}


# --------------------------------------------------
# SHIPMENT ENDPOINTS
# --------------------------------------------------

@app.get(
    "/shipments",
    response_model=list[ShipmentResponse],
    summary="List shipments",
    description="Returns the shipment records currently stored in the database.",
    tags=["Shipments"],
)
def get_shipments(db: Session = Depends(get_db)):
    shipments = db.query(Shipment).all()
    return shipments


@app.get(
    "/shipments/{shipment_id}",
    response_model=ShipmentResponse,
    summary="Get shipment details",
    description="Returns details for the requested shipment ID.",
    responses={
        404: {"description": "Shipment not found."},
    },
    tags=["Shipments"],
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

    if not shipment:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    return shipment


# --------------------------------------------------
# PREDICTION ENDPOINT
# --------------------------------------------------

@app.get(
    "/shipments/{shipment_id}/prediction",
    response_model=PredictionResponse,
    summary="Get shipment prediction",
    description=(
        "Returns the stored delay prediction, probability, "
        "and risk category for a shipment."
    ),
    responses={
        404: {"description": "Prediction not found."},
    },
    tags=["Predictions"],
)
def get_prediction(
    shipment_id: str,
    db: Session = Depends(get_db),
):
    prediction = (
        db.query(Prediction)
        .filter(Prediction.shipment_id == shipment_id)
        .first()
    )

    if not prediction:
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
# RECOMMENDATION ENDPOINT
# --------------------------------------------------

@app.get(
    "/shipments/{shipment_id}/alternatives",
    response_model=AlternativeResponse,
    summary="Get shipment recommendation",
    description=(
        "Generates a recommendation using the shipment's prediction "
        "and stores or updates the generated recommendation."
    ),
    responses={
        400: {
            "description": (
                "The prediction contains invalid data for "
                "recommendation generation."
            ),
        },
        404: {
            "description": "Shipment or prediction not found.",
        },
    },
    tags=["Recommendations"],
)
def get_alternatives(
    shipment_id: str,
    db: Session = Depends(get_db),
):
    # Verify that the shipment exists.
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == shipment_id)
        .first()
    )

    if not shipment:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    # Retrieve the prediction.
    prediction = (
        db.query(Prediction)
        .filter(Prediction.shipment_id == shipment_id)
        .first()
    )

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found",
        )

    if prediction.delay_probability is None:
        raise HTTPException(
            status_code=400,
            detail="Prediction probability is missing",
        )

    # Convert the risk category into the expected input.
    late_delivery_risk = (
        0 if prediction.risk_level == "No Risk" else 1
    )

    # Generate a recommendation.
    try:
        recommendation = generate_recommendation(
            order_id=shipment_id,
            late_delivery_risk=late_delivery_risk,
            prediction_probability=prediction.delay_probability,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    # Use a stable ID to prevent duplicate generated recommendations.
    alternative_id = f"REC-{shipment_id}"

    alternative = (
        db.query(Alternative)
        .filter(Alternative.alternative_id == alternative_id)
        .first()
    )

    if alternative:
        alternative.estimated_cost = recommendation.get(
            "estimated_cost"
        )
        alternative.action = recommendation["recommended_action"]
        alternative.recommendation_reason = recommendation[
            "recommendation_reason"
        ]
    else:
        alternative = Alternative(
            alternative_id=alternative_id,
            shipment_id=shipment_id,
            estimated_cost=recommendation.get("estimated_cost"),
            estimated_time=None,
            action=recommendation["recommended_action"],
            recommendation_reason=recommendation[
                "recommendation_reason"
            ],
        )

        db.add(alternative)

    db.commit()
    db.refresh(alternative)

    return {
        "alternative_id": alternative.alternative_id,
        "order_id": shipment_id,
        "recommended_action": alternative.action,
        "estimated_cost": alternative.estimated_cost,
        "recommendation_reason": alternative.recommendation_reason,
    }


# --------------------------------------------------
# SAVE DECISION ENDPOINT
# --------------------------------------------------

@app.post(
    "/shipments/{shipment_id}/decisions",
    response_model=DecisionResponse,
    summary="Save shipment decision",
    description=(
        "Validates the selected alternative and action, "
        "then saves the decision with a timestamp."
    ),
    responses={
        400: {
            "description": (
                "The selected action does not match the alternative."
            ),
        },
        404: {
            "description": (
                "Shipment or selected alternative not found."
            ),
        },
        422: {
            "description": "The request body failed validation.",
        },
    },
    tags=["Decisions"],
)
def save_decision(
    shipment_id: str,
    decision_data: DecisionRequestSchema,
    db: Session = Depends(get_db),
):
    # Verify that the shipment exists.
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == shipment_id)
        .first()
    )

    if not shipment:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    # Verify that the alternative belongs to this shipment.
    alternative = (
        db.query(Alternative)
        .filter(
            Alternative.alternative_id
            == decision_data.alternative_id,
            Alternative.shipment_id == shipment_id,
        )
        .first()
    )

    if not alternative:
        raise HTTPException(
            status_code=404,
            detail="Alternative not found for this shipment",
        )

    # Validate that the selected action matches the alternative.
    if decision_data.selected_action != alternative.action:
        raise HTTPException(
            status_code=400,
            detail="Selected action does not match the alternative",
        )

    # Save the decision with its timestamp.
    decision = Decision(
        shipment_id=shipment_id,
        alternative_id=decision_data.alternative_id,
        selected_action=decision_data.selected_action,
        decision_timestamp=datetime.utcnow(),
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return decision


# --------------------------------------------------
# RETRIEVE DECISION HISTORY
# --------------------------------------------------

@app.get(
    "/shipments/{shipment_id}/decisions",
    response_model=list[DecisionResponse],
    summary="Get shipment decision history",
    description=(
        "Returns saved decisions associated with the requested shipment. "
        "Returns an empty list if the shipment has no saved decisions."
    ),
    responses={
        404: {
            "description": "Shipment not found.",
        },
    },
    tags=["Decisions"],
)
def get_decisions(
    shipment_id: str,
    db: Session = Depends(get_db),
):
    # Verify that the shipment exists.
    shipment = (
        db.query(Shipment)
        .filter(Shipment.shipment_id == shipment_id)
        .first()
    )

    if not shipment:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    decisions = (
        db.query(Decision)
        .filter(Decision.shipment_id == shipment_id)
        .all()
    )

    return decisions