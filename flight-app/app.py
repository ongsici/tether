from fastapi import FastAPI, HTTPException
from .models.flight_model import FlightResponse, FlightRequest
from .services.flight_service import get_flight
from .utils.logging import configure_logging
from src.services.flight_service import get_flights
from src.models.flight_model import FlightRequest, FlightResponse
import logging
from typing import List

configure_logging()
logger = logging.getLogger("flight_microservice")

app = FastAPI()

# @app.get("/flight", response_model=List[FlightResponse])
# async def fetch_flight(origin_city:str, dest_city:str, num_passengers:int, dep_date:str, ret_date:str):
#     try:
#         logger.info(f"Fetching flight data from {origin_city} to {dest_city} from {dep_date} to {ret_date}")
#         flight_data = get_flights(origin_city, dest_city, num_passengers, dep_date, ret_date)
#         logger.info(f"Flight data fetched successfully from {origin_city} to {dest_city}")
#         return flight_data
#     except Exception as e:
#         logger.error(f"Error fetching flight data: {str(e)}")
#         raise HTTPException(status_code=400, detail=str(e))


@app.post("/itinerary", response_model=List[FlightResponse])  # Use POST method here
async def fetch_itinerary(request: FlightRequest):
    origin_loc = FlightRequest.flights.origin_loc_code
    dest_loc = FlightRequest.flights.destination_loc_code
    dep_date = FlightRequest.flights.departure_date
    ret_date = FlightRequest.flights.return_date
    num_passengers = FlightRequest.flights.num_passenger
    
    try:
        logger.info(f"Fetching flight data from {origin_loc} to {dest_loc} from {dep_date} to {ret_date}")
        flight_data = get_flights(origin_loc, dest_loc, num_passengers, dep_date, ret_date, FlightRequest.user_id)
        logger.info(f"Flight data fetched successfully from {origin_loc} to {dest_loc}")

        return flight_data
    
    except Exception as e:
        logger.error(f"Error fetching flight data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# sample POST request:
# curl -X 'POST' \
#   'http://127.0.0.1:8000/itinerary' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "city": "London",
#   "radius": 10,
#   "limit": 2
# }'