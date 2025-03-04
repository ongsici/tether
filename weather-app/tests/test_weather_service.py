# tests/test_weather_service.py

import pytest
from unittest.mock import patch, MagicMock
from src.services.weather_service import get_weather
from src.models.weather_model import WeatherResponse, CurrentWeather, ForecastDay

@pytest.fixture
def mock_openweather_data():
    """
    Mock data from OpenWeather's weather API (get_weather_data).
    We'll return a minimal JSON structure that your code expects.
    """
    return {
        "coord": {"lat": 51.5074, "lon": -0.1278},
        "sys": {"country": "GB", "sunrise": 1680330000, "sunset": 1680378000},
        "weather": [
            {"main": "Clouds", "description": "overcast clouds"}
        ],
        "main": {
            "temp": 12.0,
            "feels_like": 10.0,
            "pressure": 1012,
            "humidity": 60
        },
        "wind": {"speed": 3.5},
        "clouds": {"all": 90},
        "dt": 1680350000,  # current timestamp
        "name": "London"
    }

@pytest.fixture
def mock_openmeteo_data():
    """
    Mock data from Open-Meteo's forecast API (get_weather_forecast).
    daily keys must have the same length arrays if we want them processed.
    We'll offset index=0 as 'today', index=1 as 'tomorrow', etc.
    """
    return {
        "daily": {
            "time": ["2025-04-10", "2025-04-11"],
            "weather_code": [3, 45],  # day0=Overcast, day1=Fog
            "temperature_2m_max": [15.0, 17.0],
            "temperature_2m_min": [5.0, 7.0],
            "sunrise": ["2025-04-10T06:15", "2025-04-11T06:14"],
            "sunset": ["2025-04-10T19:45", "2025-04-11T19:46"],
            "uv_index_max": [4.0, 5.0],
            "precipitation_probability_max": [20, 40],
            "wind_speed_10m_max": [6.0, 5.5]
        }
    }

@patch("src.services.weather_service.get_weather_forecast")
@patch("src.services.weather_service.get_weather_data")
def test_get_weather_successful(
    mock_get_weather_data,
    mock_get_weather_forecast,
    mock_openweather_data,
    mock_openmeteo_data
):
    """
    GIVEN valid data from OpenWeather and Open-Meteo
    WHEN get_weather() is called
    THEN we return a WeatherResponse with 'current' and 'forecast' keys in results.
    """
    # Arrange: define mock return values
    mock_get_weather_data.return_value = mock_openweather_data
    mock_get_weather_forecast.return_value = mock_openmeteo_data

    user_id = "testuser"
    city = "London"
    country_code = "GB"

    # Act
    response = get_weather(user_id, city, country_code)

    # Assert
    mock_get_weather_data.assert_called_once_with(city, country_code)
    lat, lon = mock_openweather_data["coord"]["lat"], mock_openweather_data["coord"]["lon"]
    mock_get_weather_forecast.assert_called_once_with(lat, lon)

    # Check the overall WeatherResponse structure
    assert isinstance(response, WeatherResponse)
    assert response.user_id == user_id
    assert "current" in response.results
    assert "forecast" in response.results

    current = response.results["current"]
    assert isinstance(current, CurrentWeather)
    assert current.city == "London"
    assert current.weather_main == "Clouds"
    assert current.temperature == 12.0

    forecast_list = response.results["forecast"]
    assert len(forecast_list) == 1, "We skip index=0 in code, so we only parse index=1? Or check code logic."
    # Or if your code starts from i=1 in the loop, maybe there's only 1 day. 
    # Adjust as needed based on how your loop is written.

    first_day = forecast_list[0]
    assert isinstance(first_day, ForecastDay)
    assert first_day.date == "2025-04-11"  # index=1
    assert first_day.weather_description == "Fog"
    assert first_day.temperature_max == 17.0

@patch("src.services.weather_service.get_weather_forecast")
@patch("src.services.weather_service.get_weather_data")
def test_get_weather_incomplete_forecast(
    mock_get_weather_data,
    mock_get_weather_forecast
):
    """
    GIVEN an incomplete daily forecast structure from Open-Meteo
    WHEN get_weather() is called
    THEN we expect an empty 'forecast' list or a warning.
    """
    mock_get_weather_data.return_value = {
        "coord": {"lat": 40.7128, "lon": -74.0060},
        "sys": {"country": "US", "sunrise": 1680330000, "sunset": 1680378000},
        "weather": [{"main": "Rain", "description": "light rain"}],
        "main": {"temp": 8.0, "feels_like": 6.0, "pressure": 1008, "humidity": 90},
        "wind": {"speed": 4.2},
        "clouds": {"all": 100},
        "dt": 1680350000,
        "name": "New York"
    }
    # Suppose daily has mismatched lengths, or is missing keys
    mock_get_weather_forecast.return_value = {
        "daily": {
            "time": ["2025-04-10"],
            # missing other required keys or lengths differ
            "weather_code": [3, 45]
        }
    }

    with pytest.raises(ValueError, match="Incomplete daily forecast data"):
        get_weather("testuser2", "New York", "US")

@patch("src.services.weather_service.get_weather_data")
def test_get_weather_raises_exception_if_openweather_fails(mock_get_weather_data):
    """
    If get_weather_data raises an exception, get_weather should let it propagate.
    """
    mock_get_weather_data.side_effect = Exception("OpenWeather error")

    with pytest.raises(Exception) as exc:
        get_weather("exc_user", "SomeCity", "XX")
    assert "Failed to fetch weather data from OpenWeather API" in str(exc.value)
