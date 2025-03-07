# tests/test_weather_endpoint.py

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

# If your FastAPI app is in src/app.py with 'app = FastAPI()', do:
from src.app import app
from src.models.weather_model import WeatherResponse

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def valid_weather_request_payload():
    """
    Matches WeatherRequest: user_id + weather (city + optional country_code).
    """
    return {
        "user_id": "testuser123",
        "weather": {
            "city": "London",
            "country_code": "GB"
        }
    }

def mock_weather_response():
    """
    Example WeatherResponse-shaped dict for a single current weather + empty forecast
    (just enough for demonstration).
    """
    return WeatherResponse(
        user_id = "testuser123",
        results = {
            "current": {
                "city": "London",
                "country_code": "GB",
                "weather_main": "Clouds",
                "weather_description": "overcast clouds",
                "temperature": 12.0,
                "feels_like": 10.0,
                "pressure": 1012,
                "humidity": 60,
                "wind_speed": 3.5,
                "cloudiness": 90,
                "timestamp": 1680350000,
                "sunrise": 1680330000,
                "sunset": 1680378000,
                "latitude": 51.5074,
                "longitude": -0.1278
            },
            "forecast": []
        }
    )

@patch("src.app.get_weather")
def test_fetch_weather_success(mock_get_weather, client, valid_weather_request_payload):
    """
    GIVEN a valid request payload
    WHEN we POST to /weather
    THEN we expect a 200 response with a WeatherResponse JSON.
    """
    # Arrange
    mock_get_weather.return_value = mock_weather_response()

    # Act
    response = client.post("/weather", json=valid_weather_request_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "testuser123"
    assert "results" in data
    assert "current" in data["results"]

    # Check if we called get_weather with the correct args
    mock_get_weather.assert_called_once_with("testuser123", "London", "GB")

@patch("src.app.get_weather")
def test_fetch_weather_raises_400_on_exception(mock_get_weather, client, valid_weather_request_payload):
    """
    GIVEN get_weather raises an exception
    WHEN we POST to /weather
    THEN we expect a 400 response with the error message.
    """
    mock_get_weather.side_effect = Exception("Some weather error")

    response = client.post("/weather", json=valid_weather_request_payload)
    assert response.status_code == 400
    assert "Some weather error" in response.json()["detail"]
    mock_get_weather.assert_called_once()

def test_fetch_weather_validation_error(client):
    """
    If we omit required fields (like 'city'),
    we expect a 422 from FastAPI's validation.
    """
    invalid_payload = {
        "user_id": "invalid"
        # missing "weather" -> "city"
    }
    response = client.post("/weather", json=invalid_payload)
    assert response.status_code == 422
    assert "detail" in response.json()
