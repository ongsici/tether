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
        logger.info(f"Calling weather_service.get_weather() for city: {request.weather.city}, country_code: {request.weather.country_code}")
        weather_data = get_weather(request.user_id, request.weather.city, request.weather.country_code)
        
        if not weather_data or not weather_data.results:
            logger.warning(f"No weather data found for city: {request.weather.city}, country_code: {request.weather.country_code}")
        else:
            logger.debug(f"Weather data fetched and processed successfully")

        return weather_data
    
    except KeyError as e:
        logger.error(f"Missing key in response: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid response structure: {str(e)}")

    except ValueError as e:
        logger.warning(f"Data validation issue: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Data issue: {str(e)}")

    except RuntimeError as e:
        logger.error(f"Service error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Service error: {str(e)}")
    
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True) # log exception traceback
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")