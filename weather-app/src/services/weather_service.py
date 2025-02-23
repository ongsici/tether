from ..utils.api_client import get_weather_data, get_weather_forecast
from ..models.weather_model import ForecastDay, CurrentWeather, WeatherResponse
from ..utils.logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger("weather_microservice")

# weather code mapping for Open-Meteo
WMO_code = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
    55: "Dense drizzle", 56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain", 66: "Light freezing rain",
    67: "Heavy freezing rain", 71: "Slight snow fall", 73: "Moderate snow fall",
    75: "Heavy snow fall", 77: "Snow grains", 80: "Slight rain showers",
    81: "Moderate rain showers", 82: "Violent rain showers", 85: "Slight snow showers",
    86: "Heavy snow showers", 95: "Thunderstorm", 96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

def get_weather(city: str, country_code: str = None) -> WeatherResponse:
    logger.info(f"Calling get_weather_data for city: {city}, country_code: {country_code}")
    data = get_weather_data(city, country_code)             # [1] fetch weather data from OpenWeather API
    lat, lon = data["coord"]["lat"], data["coord"]["lon"]   # [2] extract coordinates for Open-Meteo API
    forecast_data = get_weather_forecast(lat, lon)          # [3] fetch forecast data from Open-Meteo API

    current_weather = CurrentWeather(
        city=data["name"],
        country_code=data["sys"]["country"],
        weather_main=data["weather"][0]["main"],
        weather_description=data["weather"][0]["description"],
        temperature=data["main"]["temp"],        # Celsius
        feels_like=data["main"]["feels_like"],
        pressure=data["main"]["pressure"],       # hPa
        humidity=data["main"]["humidity"],       # %
        wind_speed=data["wind"]["speed"],        # m/s
        cloudiness=data["clouds"]["all"],        # % cloudiness
        rain_1h=data.get("rain", {}).get("1h"),  # mm/h, if available
        timestamp=data["dt"],                    # UTC
        sunrise=data["sys"]["sunrise"],
        sunset=data["sys"]["sunset"],
        latitude=lat,
        longitude=lon
    )

    daily_data = forecast_data.get("daily", {})
    forecast_list = []
    if daily_data and all(len(daily_data[key]) == len(daily_data["time"]) for key in daily_data):
        for i in range(1, len(daily_data["time"])):
            weather_code = daily_data["weather_code"][i]
            weather_description = WMO_code.get(weather_code, "Unknown") # map WMO code to description

            forecast_list.append(ForecastDay(
                date=daily_data["time"][i],
                weather_description=weather_description,
                temperature_max=daily_data["temperature_2m_max"][i],
                temperature_min=daily_data["temperature_2m_min"][i],
                sunrise=daily_data["sunrise"][i],
                sunset=daily_data["sunset"][i],
                uv_index_max=daily_data["uv_index_max"][i],
                precipitation_probability_max=daily_data["precipitation_probability_max"][i],
                wind_speed_max=daily_data["wind_speed_10m_max"][i]
            ))
    else:
        logger.warning("Incomplete or missing daily forecast data")

    logger.info(f"get_weather_data successful for city: {city}")
    return WeatherResponse(results={"current": current_weather, "forecast": forecast_list})