# SupplyPrescript — Part 1 Prediction Interface

## 1. Purpose

This document defines the interface between the Part 1 machine-learning prediction module and the downstream optimization/backend components.

Part 1 predicts whether an order is at risk of late delivery using historical order-level supply-chain data.

The prediction module is implemented in:

`src/prediction.py`

---

## 2. Modeling Level

The original dataset contains 180,519 order-item records.

For prediction, these records were aggregated to the order level, resulting in 65,752 unique orders.

Therefore, the Part 1 model operates at the **order level**.

The identifier used by Part 1 is:

`Order Id`

For the current V1 backend/optimization design, `shipment_id` may be mapped to `Order Id`.

---

## 3. Model Inputs

The prediction module requires the following order-level information.

### Categorical inputs

* `shipping_mode`
* `payment_type`
* `market`
* `order_region`
* `customer_segment`

### Numeric inputs

* `scheduled_shipping_days`
* `item_count`
* `total_quantity`
* `total_sales`
* `distinct_categories`
* `distinct_departments`

### Date input

* `order_date`

The prediction module derives the following features automatically from `order_date`:

* `order_year`
* `order_month`
* `order_day_of_week`

---

## 4. Model Output

The prediction module returns two fields:

### `predicted_risk`

Binary model prediction:

* `0` = No Risk
* `1` = Risk

### `predicted_probability`

A model probability score between 0 and 1 representing the Random Forest's estimated probability for the positive class (late-delivery risk).

This score should not be interpreted as a guaranteed percentage of actual delay.

---

## 5. Classification Threshold

The selected Part 1 classification threshold is:

`0.40`

The decision rule is:

```text
predicted_probability >= 0.40
        → predicted_risk = 1

predicted_probability < 0.40
        → predicted_risk = 0
```

The threshold was selected using the validation data after evaluating the precision-recall trade-off.

A threshold of 0.30 produced very high recall but classified almost all validation orders as risky. A threshold of 0.40 provided a more balanced operational trade-off while maintaining substantially higher recall than the default 0.50 threshold.

---

## 6. Model

The current reusable prediction module uses:

**Random Forest Classifier**

Configuration:

* `n_estimators = 200`
* `max_depth = 12`
* `min_samples_leaf = 5`
* `random_state = 42`
* `n_jobs = -1`

Preprocessing includes:

* median imputation for numeric variables
* most-frequent imputation for categorical variables
* one-hot encoding for categorical variables
* `handle_unknown = "ignore"`

---

## 7. Leakage Prevention

The following fields were excluded from model inputs because they contain information that would not be available appropriately at prediction time or directly reveal the outcome:

* `Delivery Status`
* `Days for shipping (real)`
* actual shipping/delivery date information

`Delivery Status` was specifically excluded because it directly determines the historical late-delivery target and would cause target leakage.

---

## 8. Relationship with Optimization Rules

The ML classification threshold and optimization decision thresholds are separate concepts.

### Part 1 ML threshold

```text
prediction_probability >= 0.40
        → predicted_risk = 1
```

### V1 Optimization Rule 4

The current V1 optimization prototype defines:

```text
late_delivery_risk = 1
AND
prediction_probability > 0.90
        → recommended_action = Air Freight
```

Therefore, the optimization threshold of `0.90` does **not** replace the Part 1 ML threshold of `0.40`.

The two thresholds serve different purposes:

* `0.40` determines the model's binary risk classification.
* `0.90` is a downstream optimization/business-rule threshold.

The optimization rule remains a configurable V1 prototype assumption and may be revised after team review.

---

## 9. Backend/Optimization Interface

For the current V1 integration, the following information should be available to the downstream components:

| Field                    | Meaning                                             |
| ------------------------ | --------------------------------------------------- |
| `order_id`               | Order identifier corresponding to Part 1 `Order Id` |
| `late_delivery_risk`     | Model-predicted binary risk: 0 = No Risk, 1 = Risk  |
| `prediction_probability` | Model probability score between 0 and 1             |

The downstream optimization component can then return:

| Field                   | Meaning                                           |
| ----------------------- | ------------------------------------------------- |
| `order_id`              | Order identifier                                  |
| `recommended_action`    | Optimization recommendation                       |
| `estimated_cost`        | Estimated cost associated with the recommendation |
| `recommendation_reason` | Explanation of the recommendation                 |

---

## 10. Terminology Note

The historical dataset contains a field named:

`late_delivery_risk`

In the training dataset, this field represents the **historical ground-truth target**.

For the downstream V1 interface, `late_delivery_risk` refers to the **model-predicted risk**.

To avoid confusion during implementation, the distinction should be understood as:

```text
Historical data:
late_delivery_risk
        ↓
actual training target

Model output:
predicted_risk
        ↓
model prediction

V1 downstream interface:
late_delivery_risk
        ↓
model-predicted binary risk
```

The underlying meanings should not be mixed during model training or evaluation.

---

## 11. Current Limitations

The current Part 1 model:

* predicts binary late-delivery risk
* does not predict the number of days an order will be delayed
* does not estimate financial loss
* does not select an alternative supplier
* does not determine transportation cost
* does not perform optimization
* does not guarantee that a predicted-risk order will actually be late

Those responsibilities belong to the downstream optimization/backend components.

---

## 12. Implementation Reference

Reusable prediction code:

`src/prediction.py`

Module test:

`notebooks/17_test_prediction_module.py`

The module has been successfully tested using the real processed order-level dataset.

Test output contains:

* `predicted_risk`
* `predicted_probability`
