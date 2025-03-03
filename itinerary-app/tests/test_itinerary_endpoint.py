# tests/test_itinerary_endpoint.py

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def valid_request_payload():
    """
    A sample payload matching ItineraryRequest:
    {
        "user_id": "testuser123",
        "itinerary": {
            "city": "London",
            "radius": 10,
            "limit": 5
        }
    }
    """
    return {
        "user_id": "testuser123",
        "itinerary": {
            "city": "London",
            "radius": 10,
            "limit": 5
        }
    }

def mock_itinerary_response():
    """
    Example of the ItineraryResponse we might return from get_city_activities.
    """
    return {
        "user_id": "testuser123",
        "results": [
            {
                "city": "London",
                "activity_id": "ACT_1",
                "activity_name": "London Eye",
                "activity_details": "A giant Ferris wheel...",
                "price_amount": "25.0",
                "price_currency": "GBP",
                "pictures": "https://example.com/london_eye.jpg"
            }
        ]
    }

@patch("app.get_city_activities")
def test_fetch_itinerary_success(mock_get_city_activities, client, valid_request_payload):
    """
    GIVEN a valid JSON request body
    WHEN we POST to /itinerary
    THEN we should get a 200 response and a valid ItineraryResponse
    """
    # Arrange
    mock_get_city_activities.return_value = mock_itinerary_response()

    # Act
    response = client.post("/itinerary", json=valid_request_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "testuser123"
    assert len(data["results"]) == 1
    assert data["results"][0]["activity_name"] == "London Eye"

    mock_get_city_activities.assert_called_once_with(
        "testuser123",
        "London",
        10,
        5
    )

@patch("app.get_city_activities")
def test_fetch_itinerary_error_handling(mock_get_city_activities, client, valid_request_payload):
    """
    GIVEN a valid request, but get_city_activities raises an exception
    WHEN we POST to /itinerary
    THEN we should get a 400 response with the exception message.
    """
    mock_get_city_activities.side_effect = Exception("Something went wrong in itinerary")

    response = client.post("/itinerary", json=valid_request_payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Something went wrong in itinerary"
    mock_get_city_activities.assert_called_once()


def test_fetch_itinerary_validation_error(client):
    """
    GIVEN a POST request missing required fields (e.g. missing 'itinerary')
    WHEN we call /itinerary
    THEN we should get a 422 validation error from FastAPI.
    """
    invalid_payload = {
        "user_id": "testuser123"
        # "itinerary" is missing
    }

    response = client.post("/itinerary", json=invalid_payload)
    assert response.status_code == 422
    assert "detail" in response.json()
