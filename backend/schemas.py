from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ShipmentResponse(BaseModel):
    """Details returned for a shipment."""

    shipment_id: str = Field(
        description="Unique identifier of the shipment.",
        examples=["SHP001"],
    )
    origin: str = Field(
        description="Shipment origin location.",
        examples=["Bengaluru"],
    )
    destination: str = Field(
        description="Shipment destination location.",
        examples=["Mumbai"],
    )
    planned_delivery_date: Optional[date] = Field(
        default=None,
        description="Planned delivery date.",
    )
    actual_delivery_date: Optional[date] = Field(
        default=None,
        description="Actual delivery date, if available.",
    )


class PredictionResponse(BaseModel):
    """Shipment delay prediction and risk information."""

    shipment_id: str = Field(
        description="Shipment identifier associated with the prediction.",
        examples=["SHP001"],
    )
    delay_days: Optional[int] = Field(
        default=None,
        description="Predicted number of delay days.",
    )
    delay_label: Optional[str] = Field(
        default=None,
        description="Prediction label, such as Delayed.",
        examples=["Delayed"],
    )
    delay_probability: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Predicted delay probability between 0 and 1.",
        examples=[0.82],
    )
    risk_level: Optional[str] = Field(
        default=None,
        description="Risk category assigned to the shipment.",
        examples=["High"],
    )


class AlternativeResponse(BaseModel):
    """Recommendation generated for a shipment."""

    alternative_id: str = Field(
        description="Identifier of the generated alternative.",
        examples=["REC-SHP001"],
    )
    order_id: str = Field(
        description="Shipment identifier used by the recommendation module.",
        examples=["SHP001"],
    )
    recommended_action: str = Field(
        description="Action recommended for the shipment.",
        examples=["Alternate Supplier"],
    )
    estimated_cost: Optional[float] = Field(
        default=None,
        description="Estimated cost, if available.",
    )
    recommendation_reason: str = Field(
        description="Explanation for the recommended action.",
    )


class DecisionResponse(BaseModel):
    """A saved user decision for a shipment."""

    decision_id: int = Field(
        description="Unique database identifier of the saved decision.",
    )
    shipment_id: str = Field(
        description="Shipment associated with the decision.",
        examples=["SHP001"],
    )
    alternative_id: str = Field(
        description="Identifier of the selected alternative.",
        examples=["ALT001"],
    )
    selected_action: str = Field(
        description="Action selected by the user.",
        examples=["Use alternate carrier"],
    )
    decision_timestamp: datetime = Field(
        description="Date and time when the decision was saved.",
    )


class DecisionRequestSchema(BaseModel):
    """Request body used to save a shipment decision."""

    alternative_id: str = Field(
        min_length=1,
        description="ID of an existing alternative belonging to this shipment.",
        examples=["ALT001"],
    )
    selected_action: str = Field(
        min_length=1,
        description="Action associated with the selected alternative.",
        examples=["Use alternate carrier"],
    )

    model_config = ConfigDict(str_strip_whitespace=True)