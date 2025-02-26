from fastapi import FastAPI, HTTPException
from typing import List
from src.models.itinerary_model import ItineraryRequest, ItineraryResponse
from src.services.itinerary_service import get_city_activities
from src.utils.configure_logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger("itinerary_microservice")

app = FastAPI()

# endpoint to fetch activities for the given user_id, city, radius, limit
@app.post("/itinerary", response_model=ItineraryResponse)  # Use POST method here
async def fetch_itinerary(request: ItineraryRequest):
    try:
        city = request.itinerary.city
        radius = request.itinerary.radius
        limit = request.itinerary.limit

        logger.info(f"Fetching activities for city: {city}")
        activities = get_city_activities(request.user_id, city, radius, limit)
        logger.info(f"Itinerary data fetched successfully for city: {city}")

        return activities
    
    except Exception as e:
        logger.error(f"Error fetching itinerary data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# @app.get("/itinerary", response_model=ItineraryResponse)
# async def fetch_itinerary(user_id: str, city: str, radius: int = 10, limit: int = 5):
#     try:
#         logger.info(f"Fetching activities for city: {city}")
#         activities = get_city_activities(user_id, city, radius, limit)
#         logger.info(f"Itinerary data fetched successfully for city: {city}")
        
#         return activities
    
#     except Exception as e:
#         logger.error(f"Error fetching itinerary data: {str(e)}")
#         raise HTTPException(status_code=400, detail=str(e))

# sample GET request: http://127.0.0.1:7000/itinerary?user_id=gphang&city=London&radius=10&limit=2