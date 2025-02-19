import os
import requests
from dotenv import load_dotenv

load_dotenv() # load environment variable(s)

AMADEUS_API_TOKEN = os.getenv("AMADEUS_API_TOKEN")

# Amadeus API, flight offers
def get_flight_data(origin_loc_code: str, destination_loc_code: str, num_passenger: int, 
                    departure_date: str, return_date: str) -> dict:
    headers = {
        "Authorization": f"Bearer {AMADEUS_API_TOKEN}"
    }
    AMADEUS_URL = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin_loc_code}&destinationLocationCode={destination_loc_code}&departureDate={departure_date}&returnDate={return_date}&adults={num_passenger}&max=50"

    response = requests.get(AMADEUS_URL, headers=headers)
    response.raise_for_status() # Should we change this to return some error message instead?
    return response.json()


get_flight_data("a", "b", 2, "2025-02-23", "2025-02-26")





