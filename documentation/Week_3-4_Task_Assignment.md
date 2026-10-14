# SupplyPrescript — Week 3–4 Task Assignment

**Project:** SupplyPrescript — Supply Chain Risk Prediction and Optimization  
**Planning document date:** 14 October 2026  
**Project team:** 4 members  
**Team Lead:** Arshin Sheikh

## 1. Objective

The objective of Weeks 3–4 is to improve the integration of all four project components, validate the end-to-end workflow, resolve implementation issues, and prepare the project for demonstration and final submission.

Each team member is responsible for completing their assigned component, documenting implementation decisions, testing their work, and coordinating dependencies with the other members.

## 2. Task Allocation

### Member 1 — Arshin Sheikh
**Component: Part 1 — Data Preparation and Prediction**

Responsibilities:
- Review the prepared order-level dataset and data-quality checks.
- Complete model comparison, feature-importance analysis, and threshold evaluation.
- Finalize the reusable prediction module and test its output.
- Document model inputs, outputs, evaluation metrics, limitations, and data-leakage prevention.
- Share the agreed prediction interface and sample prediction outputs with the optimization and backend members.
- Support end-to-end integration and prepare explanations for model-related viva questions.

**Expected deliverables:**
- Reproducible data-preparation and model-evaluation scripts.
- Reusable prediction module.
- Prediction output CSV for integration testing.
- Prediction interface documentation and model evaluation summary.

### Member 2 — Abhishek
**Component: Part 2 — Optimization and Alternative Actions**

Responsibilities:
- Develop and refine the optimization logic using the agreed prediction interface.
- Implement and document the available actions, including No Action, Monitor Shipment, Alternate Supplier, and Air Freight.
- Validate business rules and ensure the action-selection conditions are explicit.
- Test the optimization logic using sample and model-generated prediction records.
- Coordinate the input/output contract with the prediction and backend components.
- Document assumptions, cost-estimation logic, and limitations.

**Expected deliverables:**
- Working optimization module.
- Documented business rules and action-selection logic.
- Sample outputs and test cases.
- Integration-ready interface for the backend.

### Member 3 — Chaitra
**Component: Part 3 — Backend and Database**

Responsibilities:
- Develop and refine the backend and database components.
- Define how order data, prediction results, and optimization recommendations are received and represented.
- Integrate the prediction and optimization components through the agreed interfaces.
- Validate input fields, data types, and error handling.
- Test the backend using sample records and coordinate integration issues with the relevant team members.
- Document setup instructions and backend endpoints or functions, as applicable.

**Expected deliverables:**
- Working backend/database component.
- Defined data flow and interface documentation.
- Integration and validation test results.
- Setup and execution instructions.

### Member 4 — Shravani
**Component: Part 4 — Frontend**

Responsibilities:
- Develop and refine the user interface for SupplyPrescript.
- Present relevant order information, predicted risk, and recommended actions clearly.
- Coordinate with the backend member to connect the interface to the agreed API or data flow.
- Validate loading, empty, invalid, and error states where applicable.
- Test the interface with realistic sample outputs and improve usability.
- Prepare the frontend for the final project demonstration.

**Expected deliverables:**
- Working frontend interface.
- Integration with the backend, where available.
- Screens or views for displaying risk and recommended actions.
- Frontend testing notes and run instructions.

## 3. Week 3 — Refinement and Component Testing

All members should:
- Review progress and resolve outstanding issues in their assigned component.
- Test their component independently before integration.
- Document assumptions, known limitations, and required inputs.
- Share sample data and output formats with dependent team members.
- Commit completed work to the appropriate Git branch with clear commit messages.
- Report blockers early so that integration is not delayed.

**Milestone:** Each component has a working version, documented interfaces, and basic test evidence.

## 4. Week 4 — Integration and Final Preparation

All members should:
- Integrate their components using the agreed input/output formats.
- Run an end-to-end test from order data through prediction and recommendation to presentation.
- Resolve integration errors and verify that displayed outputs match the underlying results.
- Update the README and relevant technical documentation.
- Prepare a demonstration workflow and explain the implementation of their assigned component.
- Review the project report, repository, and submission materials before the deadline.

**Milestone:** An integrated, demonstrable project with documented limitations and reproducible execution instructions.

## 5. Integration Contract

The team should use consistent field names and meanings across components.

For the current V1 prediction-to-optimization interface:

- `order_id`: identifies the order.
- `late_delivery_risk`: predicted risk class, where `0` means No Risk and `1` means Risk.
- `prediction_probability`: model-generated probability score for the positive risk class.
- `recommended_action`: action selected by the optimization component.
- `estimated_cost`: estimated cost associated with the recommendation, where applicable.
- `recommendation_reason`: explanation for the selected action.

The historical target in the training dataset must not be confused with the model-generated prediction. Integration testing should use the prediction module's output when testing downstream decisions.

The team must confirm and document any changes to field names, thresholds, business rules, or cost assumptions before treating the interface as final.

## 6. Team Coordination and Progress Tracking

- Each member remains responsible for their assigned component and its documentation.
- Members should communicate dependencies and blockers promptly.
- Integration changes must be coordinated with the affected members.
- Git commits should describe actual completed work; no backdating or artificial commits.
- The team should review the integrated workflow together before the final demonstration.

## 7. Completion Criteria

The Week 3–4 work will be considered ready for final review when:

- All four components have working implementations or clearly documented remaining limitations.
- The agreed interfaces are consistent.
- The end-to-end workflow has been tested with representative records.
- Test results, setup instructions, and known limitations are documented.
- The repository and project report reflect the actual implementation.
- The team is prepared to explain its technical decisions and demonstrate the project.

**Prepared by:** Arshin Sheikh  
**Role:** Team Lead — SupplyPrescript