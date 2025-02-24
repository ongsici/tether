import os
from dotenv import load_dotenv
import requests
from src.utils.api_refresh_token import get_valid_token

load_dotenv()  # Load API credentials from .env

# City (OpenWeather): get city's geocode (latitude, longitude)
def get_city_geocode(keyword: str) -> dict:
    OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
    OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

    params = {
        "q": keyword,  # City name
        "appid": OPENWEATHER_KEY  # API key
    }

    response = requests.get(OPENWEATHER_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if "coord" in data:
            # Extract latitude and longitude
            latitude = data["coord"]["lat"]
            longitude = data["coord"]["lon"]
            # print(f"Latitude: {latitude}, Longitude: {longitude}")
            return latitude, longitude
        else:
            print(f"Error: No coordinates found for city {keyword}")
            return None, None
    else:
        print(f"Error {response.status_code}: {response.json()}")
        response.raise_for_status()
        return None, None


# Activities (Amadeus): finding activities based on geocode
def get_activities(latitude: float, longitude: float, radius: int) -> dict:
    AMADEUS_URL = f"https://test.api.amadeus.com/v1/shopping/activities"

    headers = {
        "accept": "application/vnd.amadeus+json",
        "Authorization": f"Bearer {get_valid_token()}"
    }
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius             # TODO: check if user should input? (in km, can be from 0-20)
    }

    response = requests.get(AMADEUS_URL, headers=headers, params=params)

    if response.status_code == 401:  # Handle token expiration
        print("Token expired, refreshing...")
        headers["Authorization"] = f"Bearer {get_valid_token()}"
        response = requests.get(AMADEUS_URL, headers=headers, params=params)
    elif response.status_code == 200:
        data = response.json()
        # print("API Response:")
        # print(data)
        return data
    else:
        print(f"Error {response.status_code}: {response.json()}")
        response.raise_for_status()


# for debugging
# if __name__ == "__main__":
#     get_activities(41.397158, 2.160873, 41.394582, 2.177181)
#     get_city_geocode("London")