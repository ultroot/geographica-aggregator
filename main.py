from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI(title="Geographica Travels Aggregator")

# CORS Policy to allow the decoupled HTML frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search_flights(origin: str, destination: str):
    # Strict 3-letter IATA code validation
    if not re.match(r"^[A-Z]{3}$", origin.upper()) or not re.match(r"^[A-Z]{3}$", destination.upper()):
        raise HTTPException(status_code=400, detail="System Error: IATA codes must be exactly 3 letters.")
    
    # Mock B2B Vendor Aggregation Logic
    return {
        "flight_options": [
            {"origin": origin.upper(), "destination": destination.upper(), "date": "2026-06-15", "price": 450},
            {"origin": origin.upper(), "destination": destination.upper(), "date": "2026-06-15", "price": 480}
        ]
    }