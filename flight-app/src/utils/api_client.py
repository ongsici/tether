import requests
from api_token_refresh import get_valid_token

# Amadeus API, flight offers
def get_flight_data(origin_loc_code: str, destination_loc_code: str, num_passenger: int, 
                    departure_date: str, return_date: str) -> dict:
    AMADEUS_URL = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin_loc_code}&destinationLocationCode={destination_loc_code}&departureDate={departure_date}&returnDate={return_date}&adults={num_passenger}&max=5"

    headers = {
        "Authorization": f"Bearer {get_valid_token()}"
    }

    response = requests.get(AMADEUS_URL, headers=headers)
    if response.status_code == 401:
        print("Token expired, refreshing...")
        headers["Authorization"] = f"Bearer {get_valid_token()}"
        response = requests.get(AMADEUS_URL, headers=headers)
    elif response.status_code == 200:
        print(response.text)
        data = response.json()
        return data
    else:
        print(f"Error {response.status_code}: {response.json()}")
        response.raise_for_status()


# get_flight_data("SYD", "SIN", 2, "2025-02-23", "2025-02-26")





