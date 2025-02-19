from fastapi import FastAPI, HTTPException
from .models.flight_model import FlightResponse, FlightRequest
from .services.flight_service import get_flight
from .utils.logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger("flight_microservice")

app = FastAPI()

# endpoint to fetch weather data for given city and optional country code
@app.post("/flight", response_model=FlightResponse)
async def fetch_flight(request: FlightRequest):
    try:
        logger.info(f"Fetching flight data for city: {request.city}, country_code: {request.country_code}")
        flight_data = get_flight(request.city, request.country_code)
        logger.info(f"Flight data fetched successfully for city: {request.city}")
        return flight_data
    except Exception as e:
        logger.error(f"Error fetching flight data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))