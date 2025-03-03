from fastapi import FastAPI, HTTPException
from src.utils.custom_logging import configure_logging
from src.services.flight_service import get_flights
from src.models.flight_model import FlightRequest, FlightResponse
import logging

app = FastAPI()

@app.post("/flight", response_model=FlightResponse)
async def fetch_flight(request: FlightRequest):
    configure_logging()
    logger = logging.getLogger("flight_microservice")
    
    """Fetch flight data based on user request"""
    
    origin_loc = request.flights.origin_loc_code
    dest_loc = request.flights.destination_loc_code
    dep_date = request.flights.departure_date
    ret_date = request.flights.return_date
    num_passengers = request.flights.num_passenger
    
    # Log high-level request details at INFO
    logger.info(
        f"Received flight request from user_id={request.user_id} | "
        f"Origin={origin_loc}, Destination={dest_loc}, "
        f"Departure={dep_date}, Return={ret_date}, Passengers={num_passengers}"
    )

    # Log full request payload at DEBUG level for deeper troubleshooting (optional)
    logger.debug(f"Complete request payload: {request.dict()}")

    try:
        logger.info("Calling flight_service.get_flights() to fetch flight data...")
        flight_data = get_flights(origin_loc, dest_loc, num_passengers, dep_date, ret_date, request.user_id)
        logger.info("Successfully retrieved flight data.")

        # Log how many flight options we got at INFO
        if flight_data and flight_data.results:
            logger.info(
                f"Number of flight options retrieved: {len(flight_data.results)} "
                f"for user_id={request.user_id}"
            )
        else:
            logger.warning(
                f"No flight options found for user_id={request.user_id}. "
                f"Request details: origin={origin_loc}, dest={dest_loc}, "
                f"departure_date={dep_date}, return_date={ret_date}"
            )

        # Optionally log the entire response at DEBUG
        logger.debug(f"FlightResponse data: {flight_data}")

        return flight_data
    
    except Exception as e:
        # Include exception details at ERROR; exc_info=True can give a traceback
        logger.error("Error fetching flight data.", exc_info=True)
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
#              "num_passenger": "1"
#          },
#          "user_id": "testuser123"
#      }' \
#      http://0.0.0.0:9000/flight