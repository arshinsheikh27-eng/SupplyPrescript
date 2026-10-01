# SupplyPrescript — Week 1–2 Team Task Assignment

**Project:** SupplyPrescript
**Review:** Mid-Week Review
**Team:** Arshin Sheikh, Abhishek Guddetwar, Chaitra Kelaginamani, Chinna Bairi Shravani

## Week 1 — Project Foundation

### Arshin Sheikh — Part 1: Data Preparation & Prediction

* Select and document a suitable shipment dataset.
* Prepare a draft data dictionary.
* Inspect rows, columns, data types, missing values, duplicates, and distributions.
* Define the shipment-delay target based on available data.
* Identify possible data leakage.
* Prepare the initial data-cleaning pipeline.
* Share proposed model inputs and target with the team.

**Output:** Dataset/source notes, data dictionary, initial EDA, cleaning plan, and target definition.

### Abhishek Guddetwar — Part 2: Optimization & Alternative Actions

* Study possible actions for handling predicted shipment delays.
* Define the initial optimization approach and decision variables.
* Identify cost, service-level, budget, and inventory assumptions.
* Coordinate prediction requirements with Part 1.

**Output:** Initial optimization approach, assumptions, and alternative-action plan.

### Chaitra Kelaginamni — Part 3: Backend & Database

* Plan the backend architecture and database structure.
* Identify required tables and API endpoints.
* Define how prediction and optimization modules will connect to the backend.

**Output:** Initial backend/database design and API plan.

### Chinna Bairi Shravani — Part 4: Frontend

* Plan the user interface and required screens.
* Design the shipment-input, prediction-result, and recommendation sections.
* Coordinate frontend requirements with backend, ML, and optimization modules.

**Output:** Initial UI structure and integration requirements.

---

## Week 2 — Mid-Review Preparation

### Arshin Sheikh — Part 1: Baseline Model

* Complete the first round of data cleaning and document important exclusions.
* Prepare a reproducible train/test evaluation approach.
* Ensure post-delivery information is not used as a prediction feature.
* Build the baseline delay-risk classifier.
* Evaluate using confusion matrix, precision, recall, F1-score, and accuracy.
* Prepare sample prediction output and share the agreed format with the team.

**Output:** Cleaned/prepared dataset, baseline model, evaluation results, and sample prediction output.

### Abhishek Guddetwar — Part 2: Optimization

* Develop the initial optimization/recommendation logic.
* Define configurable cost, budget, service-level, and inventory assumptions.
* Define optimization inputs and outputs.
* Coordinate integration requirements with the backend and prediction module.

**Output:** Initial optimization prototype and documented assumptions.

### Chaitra Kelaginamani — Part 3: Backend & Database

* Implement the initial backend/database structure.
* Prepare prediction and optimization API structures.
* Establish the integration path between frontend, prediction, optimization, and database components.

**Output:** Initial backend/database implementation and API structure.

### Chinna Bairi Shravani — Part 4: Frontend

* Implement the initial frontend structure.
* Create shipment/order input and prediction-result sections.
* Prepare the recommendation display.
* Connect or prepare frontend integration with the backend.

**Output:** Initial functional frontend and integration structure.

---

## Mid-Review Expected State

By the end of Week 2, the team should be able to demonstrate:

```text
Shipment Input
      ↓
Backend
      ↓
Delay-Risk Prediction
      ↓
Optimization / Alternative Action
      ↓
Frontend Result
```

Each member should also maintain meaningful Git commits and be able to explain their own contribution, implementation decisions, results, and limitations during the review.
