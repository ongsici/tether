import logging
import requests
from .api_token_refresh import get_valid_token

logger = logging.getLogger("flight_microservice")

def get_flight_data(
    origin_loc_code: str,
    destination_loc_code: str,
    num_passenger: str,
    departure_date: str,
    return_date: str
) -> dict:
    """
    Fetch flight data from the Amadeus API for the given parameters.

    :param origin_loc_code: IATA code of the origin airport
    :param destination_loc_code: IATA code of the destination airport
    :param num_passenger: Number of passengers (adults)
    :param departure_date: Departure date in 'YYYY-MM-DD'
    :param return_date: Return date in 'YYYY-MM-DD'
    :return: Parsed JSON response from Amadeus as a dictionary
    :raises requests.exceptions.HTTPError: For any non-200 status codes
    """
    
    # Build the request URL
    AMADEUS_URL = (
        "https://test.api.amadeus.com/v2/shopping/flight-offers?"
        f"originLocationCode={origin_loc_code}&destinationLocationCode={destination_loc_code}&"
        f"departureDate={departure_date}&returnDate={return_date}&adults={num_passenger}&max=5"
    )

    # Prepare headers with a valid token
    token = get_valid_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    logger.info(
        f"Attempting to fetch flight data from Amadeus: "
        f"origin={origin_loc_code}, destination={destination_loc_code}, "
        f"departure_date={departure_date}, return_date={return_date}, passengers={num_passenger}"
    )

    logger.debug(f"Amadeus GET URL: {AMADEUS_URL}")
    logger.debug(f"Request headers: {headers}")

    try:
        response = requests.get(AMADEUS_URL, headers=headers)
        logger.debug(f"Initial response status code: {response.status_code}")

        if response.status_code == 401:
            logger.warning("Received 401 Unauthorized from Amadeus. Refreshing token and retrying...")
            new_token = get_valid_token()  # Attempt to get/refresh token
            headers["Authorization"] = f"Bearer {new_token}"
            response = requests.get(AMADEUS_URL, headers=headers)
            logger.debug(f"Retry response status code after token refresh: {response.status_code}")

        if response.status_code == 200:
            logger.info("Successfully retrieved flight data from Amadeus (status 200).")
            logger.debug(f"Amadeus response body: {response.text}")
            data = response.json()
            return data
        else:
            logger.error(
                f"Error fetching data from Amadeus. Status code: {response.status_code}, "
                f"Response: {response.text}"
            )
            response.raise_for_status()

    except requests.exceptions.RequestException as req_err:
        logger.error("Exception occurred while requesting data from Amadeus.", exc_info=True)
        raise req_err





