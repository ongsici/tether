from pydantic import BaseModel
from typing import List, Optional

# request model for endpoint
class WeatherRequest(BaseModel):
    city: str
    country_code: str = None  # optional field

# model for single forecast day
class ForecastDay(BaseModel):
    date: str
    weather_code: int
    temperature_max: float
    temperature_min: float
    sunrise: str
    sunset: str
    uv_index_max: Optional[float] = None
    precipitation_probability_max: int
    wind_speed_max: float

# response model for endpoint
class WeatherResponse(BaseModel):
    city: str
    country_code: str
    weather_main: str
    weather_description: str
    weather_icon: str
    temperature: float
    feels_like: float
    pressure: int
    humidity: int
    wind_speed: float
    cloudiness: int
    rain_1h: Optional[float] = None # if available
    timestamp: int
    sunrise: int
    sunset: int
    latitude: float
    longitude: float
    forecast: List[ForecastDay] = []