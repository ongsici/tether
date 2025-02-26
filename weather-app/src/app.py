from fastapi import FastAPI, HTTPException
from .models.weather_model import WeatherRequest, WeatherResponse
from .services.weather_service import get_weather
from .utils.logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger("weather_microservice")

app = FastAPI()

# endpoint to fetch weather data for given city and optional country code
@app.post("/weather", response_model=WeatherResponse)
async def fetch_weather(request: WeatherRequest):
    try:
        logger.info(f"Fetching weather data for city: {request.weather.city}, country_code: {request.weather.country_code}")
        weather_data = get_weather(request.user_id, request.weather.city, request.weather.country_code)
        logger.info(f"Weather data fetched successfully for city: {request.weather.city}")
        return weather_data
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))