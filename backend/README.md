# SupplyPrescript Backend

Backend and database module for the SupplyPrescript shipment delay prediction and decision-support system.

## 1. Overview

SupplyPrescript is a decision-support system designed to help users respond to potential shipment delays. The backend provides APIs for:

* Retrieving shipment information.
* Retrieving shipment delay predictions.
* Generating shipment recommendations.
* Persisting generated alternatives.
* Saving user-selected decisions.
* Retrieving saved decisions.

The backend supports the project's closed-loop workflow by recording selected actions for later outcome evaluation.

### Technology Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite for local development
* Pydantic
* Pytest
* Uvicorn

## 2. Project Structure

```text
backend/
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── init_db.py
├── seed_data.py
├── requirements.txt
├── supplyprescript.db
├── optimization/
│   ├── __init__.py
│   └── optimization_model.py
└── tests/
    ├── test_api.py
    └── test_optimization.py
```

**Main files and directories:**

* `main.py`: Defines the FastAPI application and API endpoints.
* `config.py`: Configures the database URL.
* `database.py`: Creates the SQLAlchemy engine, session factory, and declarative base.
* `models.py`: Defines the database models and their relationships.
* `schemas.py`: Defines Pydantic request and response schemas.
* `init_db.py`: Creates database tables.
* `seed_data.py`: Adds sample shipment, prediction, and alternative records.
* `optimization/optimization_model.py`: Implements the recommendation logic.
* `tests/`: Contains automated API and recommendation tests.

The database file is used for local development. Its actual location depends on the configured database URL and the application's working directory.

## 3. Backend Architecture

The backend connects the API, recommendation logic, and database.

```text
             Frontend / API Client
                      |
                      v
                FastAPI API
                  main.py
                      |
          +-----------+-----------+
          |                       |
          v                       v
   Pydantic Schemas       Recommendation Module
      schemas.py          optimization_model.py
          |                       |
          +-----------+-----------+
                      |
                      v
                SQLAlchemy ORM
          database.py / models.py
                      |
                      v
                  Database
              SQLite by default
```

### Workflow

1. The client requests shipment information.
2. The backend retrieves the shipment and its prediction from the database.
3. The recommendation endpoint generates an action using the recommendation module.
4. The generated recommendation is persisted as an alternative.
5. The user submits a selected alternative and action.
6. The backend validates and saves the decision with a timestamp.
7. Saved decisions can be retrieved for a shipment.

The current recommendation rules are demonstration logic and should not be considered validated production optimization.

## 4. Database Configuration

Database configuration is defined in `config.py`.

The default database URL is:

```text
sqlite:///./supplyprescript.db
```

The backend also supports overriding the database URL using the `SUPPLYPRESCRIPT_DATABASE_URL` environment variable.

The `database.py` module provides:

* `engine`: SQLAlchemy database engine.
* `SessionLocal`: Factory for creating database sessions.
* `Base`: Declarative base used to define database models.

SQLite connections are configured to support the application's request-handling pattern.

## 5. Database Models

The SQLAlchemy models are defined in `models.py`.

### Shipments

Stores shipment details, including:

* Shipment ID
* Origin
* Destination
* Planned delivery date
* Actual delivery date, if available

### Predictions

Stores shipment delay prediction information, including:

* Shipment ID
* Predicted delay days
* Delay label
* Delay probability
* Risk level

### Alternatives

Stores recommendation information, including:

* Alternative ID
* Shipment ID
* Estimated cost, if available
* Estimated time, if available
* Recommended action
* Recommendation reason, where available

### Decisions

Stores user-selected decisions, including:

* Decision ID
* Shipment ID
* Selected alternative ID
* Selected action
* Decision timestamp

The models define relationships between shipments and their associated predictions, alternatives, and decisions.

## 6. API Endpoints

Start the backend server before calling the endpoints.

**Base URL:**

```text
http://127.0.0.1:8000
```

**Interactive API documentation:**

```text
http://127.0.0.1:8000/docs
```

### Endpoint Reference

| Method | Endpoint                                | Description                                               |
| ------ | --------------------------------------- | --------------------------------------------------------- |
| GET    | `/`                                     | Returns the API home response.                            |
| GET    | `/shipments`                            | Retrieves shipment records.                               |
| GET    | `/shipments/{shipment_id}`              | Retrieves details for a specific shipment.                |
| GET    | `/shipments/{shipment_id}/prediction`   | Retrieves the shipment's delay prediction.                |
| GET    | `/shipments/{shipment_id}/alternatives` | Generates and persists a recommendation for the shipment. |
| POST   | `/shipments/{shipment_id}/decisions`    | Saves a user-selected decision.                           |
| GET    | `/shipments/{shipment_id}/decisions`    | Retrieves saved decisions for the shipment.               |

Use Swagger UI at `/docs` to inspect endpoint schemas, submit requests, and review responses.

### Decision Request Example

The decision endpoint accepts an alternative ID and the corresponding selected action.

Example request body:

```json
{
  "alternative_id": "ALT001",
  "selected_action": "Use alternate carrier"
}
```

The alternative must exist and belong to the specified shipment. The selected action must match the action associated with the alternative.

A successful request saves the decision and its timestamp.

### Error Handling

Depending on the endpoint and the error encountered, the API can return errors for cases such as:

* Shipment not found.
* Prediction not found.
* Alternative not found.
* Alternative does not belong to the specified shipment.
* Selected action does not match the alternative.
* Invalid recommendation inputs.
* Database errors during recommendation or decision persistence.

Consult the interactive API documentation and `main.py` for endpoint-specific response details.

## 7. Recommendation Logic

The recommendation logic is implemented in:

```text
optimization/optimization_model.py
```

The recommendation function uses prediction-related inputs to determine a recommended action.

The current demonstration rules can return actions such as:

* `No Action`
* `Monitor Shipment`
* `Alternate Supplier`
* `Air Freight`

The recommendation result includes:

* Shipment/order identifier
* Recommended action
* Estimated cost, if available
* Recommendation reason

The current recommendation implementation returns no estimated cost. Consequently, the estimated cost is represented as `null` in the API response.

The alternatives endpoint persists the generated recommendation so it can be selected in the decision workflow.

**Important:** The current recommendation rules are illustrative. They have not been established as operationally optimal, and the API does not provide verified real-world supplier quotes or logistics cost estimates.

## 8. Decision Write-Back Workflow

The decision write-back feature records the user's selected action.

1. Retrieve the shipment information and delay prediction.
2. Request a recommendation.
3. Identify the alternative the user wants to select.
4. Submit the alternative ID and selected action to the decision endpoint.
5. The backend checks that the shipment and alternative exist.
6. The backend verifies that the alternative belongs to the shipment and that the selected action matches.
7. The backend saves the decision with a timestamp.
8. Retrieve the saved decisions using the decision retrieval endpoint.

This provides a record of user decisions that can support later analysis.

Saving a decision does not by itself establish whether the action improved delivery performance. Actual outcome evaluation requires delivery outcome data and additional evaluation logic.

## 9. Initialize the Database

Run commands from the backend directory.

```cmd
cd /d D:\SupplyPrescript_repo\backend
```

Create the database tables:

```cmd
venv\Scripts\python.exe init_db.py
```

The initialization script uses SQLAlchemy's `Base.metadata.create_all()` to create tables that do not already exist.

This initialization method is suitable for the current development setup. It does not replace a database migration system for managing future schema changes.

## 10. Load Demonstration Data

Run the seed script:

```cmd
venv\Scripts\python.exe seed_data.py
```

The script checks whether its sample records already exist before inserting them. Existing records are left unchanged.

### Sample Shipment

| Field                 | Value      |
| --------------------- | ---------- |
| Shipment ID           | `SHP001`   |
| Origin                | Bengaluru  |
| Destination           | Mumbai     |
| Planned delivery date | 2026-09-30 |

### Sample Prediction

| Field             | Value    |
| ----------------- | -------- |
| Shipment ID       | `SHP001` |
| Predicted delay   | 2 days   |
| Prediction label  | Delayed  |
| Delay probability | 0.82     |
| Risk level        | High     |

### Sample Alternatives

| Alternative ID | Action                        |
| -------------- | ----------------------------- |
| `ALT001`       | Use alternate carrier         |
| `ALT002`       | Continue with current carrier |

The sample alternative records also contain demonstration cost and estimated-time values.

These values are not verified supplier quotes or real-world logistics estimates.

## 11. Run the Backend API

From the backend directory, execute:

```cmd
venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to test the available endpoints.

To stop the server, press `Ctrl + C` in the terminal.

## 12. Run Automated Tests

From the backend directory, run:

```cmd
venv\Scripts\python.exe -m pytest -q
```

The test suite includes API and recommendation tests.

Check the test output to confirm that all tests pass after code or documentation changes.

## 13. Limitations and Development Notes

* SQLite is the default database for local development.
* The database URL can be overridden using `SUPPLYPRESCRIPT_DATABASE_URL`.
* Sample shipment and prediction records are demonstration data.
* Recommendation rules are illustrative and have not been validated for production use.
* Estimated cost and time values must not be interpreted as verified operational quotes.
* Database initialization creates missing tables but does not perform schema migrations.
* Decision write-back records user choices but does not independently evaluate their outcomes.
* Do not commit credentials, secrets, or sensitive operational data.

## 14. Workstream Ownership

Backend, database, and decision write-back are part of Chaitra Kelaginamani's assigned SupplyPrescript workstream.

This component integrates with the team's prediction, optimization, and frontend components through the backend API and shared shipment identifiers.
