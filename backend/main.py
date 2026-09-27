from fastapi import FastAPI

app = FastAPI(
    title="SupplyPrescript Backend API",
    description="Backend API for shipment delay prediction and decision support",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "SupplyPrescript Backend is running"
    }