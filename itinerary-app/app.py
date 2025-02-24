from fastapi import FastAPI, HTTPException
from typing import List
from src.models.itinerary_model import ItineraryRequest, ItineraryResponse
from src.services.itinerary_service import get_city_activities
from src.utils.configure_logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger("itinerary_microservice")

app = FastAPI()

# endpoint to fetch activities for the given city and optional parameters
@app.get("/itinerary", response_model=List[ItineraryResponse])
async def fetch_itinerary(city: str, radius: int = 10, limit: int = 5):
    try:
        logger.info(f"Fetching activities for city: {city}")
        activities = get_city_activities(city, radius, limit)
        logger.info(f"Itinerary data fetched successfully for city: {city}")
        
        return activities
    
    except Exception as e:
        logger.error(f"Error fetching itinerary data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# sample GET request: http://127.0.0.1:8000/itinerary?city=London&radius=10&limit=2


# @app.post("/itinerary", response_model=List[ItineraryResponse])  # Use POST method here
# async def fetch_itinerary(request: ItineraryRequest):
#     try:
#         city = request.city
#         radius = request.radius
#         limit = request.limit

#         logger.info(f"Fetching activities for city: {city}")
#         activities = get_city_activities(city, radius, limit)
#         logger.info(f"Itinerary data fetched successfully for city: {city}")

#         return activities  # Return the list of ItineraryResponse objects
    
#     except Exception as e:
#         logger.error(f"Error fetching itinerary data: {str(e)}")
#         raise HTTPException(status_code=400, detail=str(e))


# sample POST request:
# curl -X 'POST' \
#   'http://127.0.0.1:8000/itinerary' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "city": "London",
#   "radius": 10,
#   "limit": 2
# }'