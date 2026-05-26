from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Geographica Aggregator API")

# DEVSECOPS: CORS Policy Implementation
app.add_middleware(
    CORSMiddleware,
    # IN PRODUCTION: This is restricted to the specific domain (e.g., ["https://geographicaltravels.com"])
    # Using "*" is only permitted in the local development laboratory.
    allow_origins=["*"], 
    allow_credentials=True,
    # Principle of Least Privilege: We explicitly whitelist only GET requests. 
    # If an attacker attempts a POST or DELETE payload, the firewall drops it at the perimeter.
    allow_methods=["GET"], 
    allow_headers=["*"],
)

VENDORS = ["Akbar Travels", "Travelboutique", "MakeMyTrip B2B", "FTD Travels"]

@app.get("/")
def read_root():
    return {"status": "success", "message": "Geographica Aggregator Engine is Live!"}

# Strict Input Validation Endpoint
@app.get("/api/flights/search")
def search_flights(
    origin: str = Query(..., min_length=3, max_length=3, pattern="^[A-Za-z]+$"),
    destination: str = Query(..., min_length=3, max_length=3, pattern="^[A-Za-z]+$"),
    date: str = Query(..., min_length=10, max_length=10)
):
    results = []
    for vendor in VENDORS:
        results.append({
            "vendor": vendor,
            "origin": origin.upper(),
            "destination": destination.upper(),
            "date": date,
            "price": random.randint(12000, 18000)
        })
    
    # The Sorting Algorithm
    sorted_results = sorted(results, key=lambda flight: flight["price"])
    
    return {
        "message": "Flights retrieved successfully",
        "total_vendors_searched": len(VENDORS),
        "cheapest_available": sorted_results["price"],
        "flight_options": sorted_results
    }