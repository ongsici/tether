from ..utils.api_client import get_city_geocode, get_activities
from ..models.itinerary_model import ItineraryResponseObj, ItineraryResponse
from ..utils.configure_logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger("itinerary_microservice")

def get_city_activities(user_id: str, city_name: str, radius: int, limit: int = 10) -> ItineraryResponse:
    logger.info(f"Fetching city activities for user: {user_id}, city: {city_name}, radius: {radius}, limit: {limit}")

    try:
        logger.debug(f"Calling get_city_geocode for city: {city_name}")
        latitude, longitude = get_city_geocode(city_name)

        if latitude == None or longitude == None:
            logger.warning(f"Could not find geocode for city: {city_name}")
            return {"error": f"Could not find geocode for city: {city_name}"}
        logger.debug(f"Geocode found: latitude={latitude}, longitude={longitude}")
        
        logger.debug(f"Calling get_activities with lat={latitude}, long={longitude}, radius={radius}")
        data = get_activities(latitude, longitude, radius)
        if not data or "data" not in data:
            logger.error(f"get_activities returned empty data for city: {city_name}")
            return {"error": f"No activities found for city: {city_name}"}

        # limit num activities returned to given limits
        limited_data = data.get("data", [])[:limit]
        logger.debug(f"Retrieved {len(limited_data)} activities (limit: {limit})")

        itinerary_responses = []
        for activity in limited_data:
            pic = activity.get("pictures", [])

            itinerary_responses.append(ItineraryResponseObj(
                city = city_name,
                activity_id = activity.get("id", "None"),
                activity_name = activity.get("name", "No name available"),
                activity_details = activity.get("shortDescription", "No description available"),
                price_amount = activity.get("price", {}).get("amount", "0.0"),
                price_currency = activity.get("price", {}).get("currencyCode", "EUR"),
                pictures = pic[0] if pic else ""
            ))

        logger.info(f"get_activities successful for city geoCode: {latitude}, {longitude}")
        return ItineraryResponse(user_id=user_id, results=itinerary_responses)
    
    except Exception as e:
        logger.exception(f"Unexpected error while fetching city activities for {city_name}: {e}")
        return {"error": "An internal error occurred while processing your request."}
