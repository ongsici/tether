from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.weather_model import WeatherRequest, WeatherResponse
from .services.weather_service import get_weather
from .utils.logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger("weather_microservice")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tether-apim-2.azure-api.net", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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