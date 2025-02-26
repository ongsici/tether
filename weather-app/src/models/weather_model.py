from pydantic import BaseModel
from typing import List, Optional

# request model for endpoint
class WeatherRequestObj(BaseModel):
    city: str
    country_code: str = None  # optional field

class WeatherRequest(BaseModel):
    user_id: str
    weather: WeatherRequestObj

# model for single forecast day
class ForecastDay(BaseModel):
    date: str
    weather_description: str
    temperature_max: float
    temperature_min: float
    sunrise: str
    sunset: str
    uv_index_max: Optional[float] = None
    precipitation_probability_max: int
    wind_speed_max: float

# model for current weather
class CurrentWeather(BaseModel):
    city: str
    country_code: str
    weather_main: str
    weather_description: str
    temperature: float
    feels_like: float
    pressure: int
    humidity: int
    wind_speed: float
    cloudiness: int
    timestamp: int
    sunrise: int
    sunset: int
    latitude: float
    longitude: float

# response model for endpoint
class WeatherResponse(BaseModel):
    user_id: str
    results: dict