import os
import requests
from dotenv import load_dotenv

load_dotenv() # load environment variable(s)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER-API-KEY")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# OpenWeather API
def get_weather_data(city: str, country_code: str = None) -> dict:
    query = f"{city},{country_code}" if country_code else city
    params = {
        "q": query,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(OPENWEATHER_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.json()}")
        response.raise_for_status()  # raise exception for HTTP errors
        return None
    

# Open-Meteo API
def get_weather_forecast(lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min",
                  "sunrise", "sunset", "uv_index_max", "precipitation_probability_max",
                  "wind_speed_10m_max"],
        "wind_speed_unit": "ms",
        "timezone": "auto"
    }

    response = requests.get(OPEN_METEO_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.json()}")
        response.raise_for_status()