import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv() # load environment variable(s)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER-API-KEY")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

logger = logging.getLogger("weather_microservice")

# OpenWeather API
def get_weather_data(city: str, country_code: str = None) -> dict:
    query = f"{city},{country_code}" if country_code else city
    params = {
        "q": query,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(OPENWEATHER_URL, params=params)
        response.raise_for_status() # raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed OpenWeather API request: {str(e)}", exc_info=True)
        raise RuntimeError("Error fetching weather data") from e

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

    try:
        response = requests.get(OPEN_METEO_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed Open-Meteo API request: {str(e)}", exc_info=True)
        raise RuntimeError("Error fetching forecast data") from e