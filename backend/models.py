from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    shipment_id = Column(String, primary_key=True, index=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    planned_delivery_date = Column(Date, nullable=True)
    actual_delivery_date = Column(Date, nullable=True)


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(String, ForeignKey("shipments.shipment_id"), nullable=False)
    delay_days = Column(Integer, nullable=True)
    delay_label = Column(String, nullable=True)
    delay_probability = Column(Float, nullable=True)
    risk_level = Column(String, nullable=True)


class Alternative(Base):
    __tablename__ = "alternatives"

    alternative_id = Column(String, primary_key=True, index=True)
    shipment_id = Column(String, ForeignKey("shipments.shipment_id"), nullable=False)
    estimated_cost = Column(Float, nullable=True)
    estimated_time = Column(Float, nullable=True)
    action = Column(String, nullable=True)


class Decision(Base):
    __tablename__ = "decisions"

    decision_id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(String, ForeignKey("shipments.shipment_id"), nullable=False)
    alternative_id = Column(String, ForeignKey("alternatives.alternative_id"), nullable=False)
    selected_action = Column(String, nullable=False)
    decision_timestamp = Column(DateTime, nullable=False)