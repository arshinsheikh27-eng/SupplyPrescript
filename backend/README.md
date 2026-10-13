\# SupplyPrescript Backend



Backend and database module for the SupplyPrescript shipment delay prediction and decision-support system.



\## 1. Overview



The backend provides APIs for:



\- Retrieving shipment information

\- Retrieving shipment delay predictions

\- Generating optimization-based shipment recommendations

\- Persisting generated alternatives

\- Saving user-selected decisions

\- Retrieving saved decisions



The backend is implemented using:



\- FastAPI

\- SQLAlchemy

\- SQLite

\- Pydantic

\- Pytest



\## 2. Project Structure



```text

backend/

│

├── main.py

├── database.py

├── models.py

├── init\_db.py

├── seed\_data.py

├── requirements.txt

├── supplyprescript.db

│

├── optimization/

│   ├── \_\_init\_\_.py

│   └── optimization\_model.py

│

└── tests/

&#x20;   ├── test\_api.py

&#x20;   └── test\_optimization.py
# SupplyPrescript Backend

## Overview

The SupplyPrescript backend provides API endpoints for shipment details,
delay predictions, recommendations, and decision history.

The backend uses FastAPI for its REST API and SQLAlchemy for database
operations.

## Database Configuration

Database configuration is defined in `database.py`.

The current database URL is:

    sqlite:///./supplyprescript.db

This configures SQLite to use a database file named
`supplyprescript.db` relative to the backend application's working
directory.

The database module provides:

- `engine`: SQLAlchemy database engine.
- `SessionLocal`: Factory for creating database sessions.
- `Base`: Declarative base used to define database models.

Database sessions are used by API endpoints to retrieve and persist data.

## Database Models

The SQLAlchemy models are defined in `models.py`.

The main database tables are:

### Shipments

Stores shipment details, including:

- Shipment ID
- Origin
- Destination
- Planned delivery date
- Actual delivery date

### Predictions

Stores shipment delay prediction information, including:

- Shipment ID
- Predicted delay days
- Delay label
- Delay probability
- Risk level

### Alternatives

Stores recommendation information, including:

- Alternative ID
- Shipment ID
- Estimated cost
- Estimated time
- Recommended action
- Recommendation reason

### Decisions

Stores user decisions, including:

- Decision ID
- Shipment ID
- Selected alternative ID
- Selected action
- Decision timestamp

## Seed Data

The sample data initialization script is `seed_data.py`.

It prepares demonstration records used to test and demonstrate the
backend API.

The current sample data includes:

### Sample Shipment

- Shipment ID: `SHP001`
- Origin: Bengaluru
- Destination: Mumbai
- Planned delivery date: 2026-09-30

### Sample Prediction

- Shipment ID: `SHP001`
- Predicted delay: 2 days
- Prediction label: Delayed
- Delay probability: 0.82
- Risk level: High

### Sample Alternatives

The sample data includes:

- `ALT001`: Use alternate carrier
- `ALT002`: Continue with current carrier

The sample alternatives contain demonstration cost and estimated-time
values. These values should not be interpreted as verified operational
quotes.

## Initializing the Database

Run commands from the backend directory:

    cd /d D:\SupplyPrescript_repo\backend

The database schema is created using the SQLAlchemy models and the
database initialization code provided by the project.

Before running the seed script, check the implementation in
`seed_data.py` to confirm how it initializes the database and handles
existing records.

Run the seed script using the project's virtual environment:

    venv\Scripts\python.exe seed_data.py

The seed script is designed to avoid creating duplicate copies of its
sample records when run repeatedly.

## Running the Backend API

From the backend directory, run:

    venv\Scripts\python.exe -m uvicorn main:app --reload

The local API base address is:

    http://127.0.0.1:8000

Interactive API documentation is available at:

    http://127.0.0.1:8000/docs

## Running Tests

Run the backend tests from the backend directory:

    venv\Scripts\python.exe -m pytest -q

Tests cover API behavior, validation, database interactions, and
decision handling.

## Important Notes

- The SQLite database is used for local development and demonstration.
- Sample shipment and prediction values are demonstration data.
- Recommendation costs and timing estimates should not be treated as
  verified real-world operational recommendations.
- Do not commit credentials, secrets, or sensitive operational data.
