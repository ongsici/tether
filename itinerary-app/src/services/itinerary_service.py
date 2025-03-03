from ..utils.api_client import get_city_geocode, get_activities
from ..models.itinerary_model import ItineraryResponseObj, ItineraryResponse
from ..utils.configure_logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger("itinerary_microservice")

def get_city_activities(user_id: str, city_name: str, radius: int, limit: int = 10) -> ItineraryResponse:
    logger.info(f"Calling get_city_geocode for city: {city_name}")
    latitude, longitude = get_city_geocode(city_name)

    if latitude == None or longitude == None:
        return {"error": f"Could not find geocode for city: {city_name}"}

    logger.info(f"get_city_geocode successful for city: {city_name}")

    logger.info(f"Calling get_activities for city geoCode: {latitude}, {longitude}")
    data = get_activities(latitude, longitude, radius)

    # limit num activities returned to given limits
    limited_data = data.get("data", [])[:limit]

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


# for debugging
# if __name__ == "__main__":
#     response = get_city_activities("London", 10, 2)
#     print(response.dict())