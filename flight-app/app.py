from fastapi import FastAPI, HTTPException
from src.utils.custom_logging import configure_logging
from src.services.flight_service import get_flights
from src.models.flight_model import FlightRequest, FlightResponse
import logging
from typing import List

configure_logging()
logger = logging.getLogger("flight_microservice")

app = FastAPI()

@app.post("/flight", response_model=FlightResponse)
async def fetch_flight(request: FlightRequest):
    origin_loc = request.flights.origin_loc_code
    dest_loc = request.flights.destination_loc_code
    dep_date = request.flights.departure_date
    ret_date = request.flights.return_date
    num_passengers = request.flights.num_passenger
    
    try:
        logger.info(f"Fetching flight data from {origin_loc} to {dest_loc} from {dep_date} to {ret_date}")
        flight_data = get_flights(origin_loc, dest_loc, num_passengers, dep_date, ret_date, request.user_id)
        logger.info(f"Flight data fetched successfully from {origin_loc} to {dest_loc}")

        return flight_data
    
    except Exception as e:
        logger.error(f"Error fetching flight data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# sample POST request:

# curl -X POST \
#      -H "Content-Type: application/json" \
#      -d '{
#          "flights": {
#              "origin_loc_code": "SYD",
#              "destination_loc_code": "SIN",
#              "departure_date": "2025-03-10",
#              "return_date": "2025-03-17",
#              "num_passenger": 1
#          },
#          "user_id": "testuser123"
#      }' \
#      http://0.0.0.0:5000/flight