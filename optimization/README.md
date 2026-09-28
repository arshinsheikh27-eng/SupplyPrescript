# SupplyPrescript - Optimization Module

This module is responsible for generating alternative actions when a shipment is predicted to be at risk of late delivery.

## Inputs

- order_id
- late_delivery_risk
- prediction_probability

## Outputs

- recommended_action
- estimated_cost
- recommendation_reason

## Possible Actions

1. No Action
2. Monitor Shipment
3. Alternate Supplier
4. Air Freight