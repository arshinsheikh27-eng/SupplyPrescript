from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ShipmentResponse(BaseModel):
    shipment_id: str
    origin: str
    destination: str
    planned_delivery_date: Optional[date] = None
    actual_delivery_date: Optional[date] = None


class PredictionResponse(BaseModel):
    shipment_id: str
    delay_days: Optional[int] = None
    delay_label: Optional[str] = None
    delay_probability: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
    )
    risk_level: Optional[str] = None


class AlternativeResponse(BaseModel):
    alternative_id: str
    order_id: str
    recommended_action: str
    estimated_cost: Optional[float] = None
    recommendation_reason: str


class DecisionResponse(BaseModel):
    decision_id: int
    shipment_id: str
    alternative_id: str
    selected_action: str
    decision_timestamp: datetime


class DecisionRequestSchema(BaseModel):
    alternative_id: str = Field(min_length=1)
    selected_action: str = Field(min_length=1)

    model_config = ConfigDict(str_strip_whitespace=True)