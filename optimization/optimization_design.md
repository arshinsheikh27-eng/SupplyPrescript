# Optimization Design (V1)

## Input

Prediction model output:

- order_id
- late_delivery_risk
- prediction_probability

## Decision Logic

### Rule 1

If:
- late_delivery_risk = 0

Then:
- Recommended Action = No Action

### Rule 2

If:
- late_delivery_risk = 1
- prediction_probability between 0.50 and 0.75

Then:
- Recommended Action = Monitor Shipment

### Rule 3

If:
- late_delivery_risk = 1
- prediction_probability between 0.75 and 0.90

Then:
- Recommended Action = Alternate Supplier

### Rule 4

If:
- late_delivery_risk = 1
- prediction_probability greater than 0.90

Then:
- Recommended Action = Air Freight

## Output

The optimization module will return:

- order_id
- recommended_action
- estimated_cost
- recommendation_reason

## Example

Input:

order_id = 50102
late_delivery_risk = 1
prediction_probability = 0.83

Output:

recommended_action = Alternate Supplier
estimated_cost = 10000
recommendation_reason = High delay risk detected