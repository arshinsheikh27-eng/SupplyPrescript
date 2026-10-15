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

## Member 2 – Optimization & Alternative Actions: Completion Summary

### Completed Work

- Documented optimization assumptions and business rules.
- Designed the optimization recommendation workflow.
- Implemented the recommendation engine in `optimization_model.py`.
- Integrated the engine with Member 1's ML prediction output.
- Added validation for required CSV columns.
- Processed 13,151 test-order prediction records.
- Generated `data/optimization_results.csv`.
- Tested the module and pushed changes to the `member2-optimization` branch.

### Input Fields

- `Order Id` → `order_id`
- `predicted_risk` → `late_delivery_risk`
- `predicted_probability` → `prediction_probability`

### Output Fields

- `order_id`
- `recommended_action`
- `estimated_cost`
- `recommendation_reason`

### Recommendation Actions

- No Action
- Monitor Shipment
- Alternate Supplier
- Air Freight

### Current Status

The core Member 2 deliverables are complete. The optimization module is ready for backend integration testing. Further changes may be required based on team feedback or updated business rules.

**Note:** The recommendation engine currently uses rule-based logic. The business assumptions are provisional and require team approval.