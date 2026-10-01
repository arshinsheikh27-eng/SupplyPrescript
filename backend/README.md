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

