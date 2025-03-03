import pytest
from unittest.mock import patch, MagicMock
from src.services.itinerary_service import get_city_activities
from src.models.itinerary_model import ItineraryResponse, ItineraryResponseObj

@pytest.fixture
def mock_city_geocode():
    """Return a tuple (latitude, longitude) as if from get_city_geocode."""
    return (51.5074, -0.1278)  # Example lat/lon for London

@pytest.fixture
def mock_activities_response():
    """
    Example data structure as if returned by get_activities().
    We'll only include a few activities for demonstration.
    """
    return {
        "data": [
            {
                "id": "ACT_1",
                "name": "London Eye",
                "shortDescription": "A giant Ferris wheel on the South Bank of the River Thames.",
                "price": {
                    "amount": "25.0",
                    "currencyCode": "GBP"
                },
                "pictures": [
                    "https://example.com/london_eye.jpg"
                ]
            },
            {
                "id": "ACT_2",
                "name": "Tower of London",
                "shortDescription": "Historic castle located on the north bank of the River Thames.",
                "price": {
                    "amount": "30.0",
                    "currencyCode": "GBP"
                },
                "pictures": [
                    "https://example.com/tower_of_london.jpg"
                ]
            }
        ]
    }

@patch("src.services.itinerary_service.get_city_geocode")
@patch("src.services.itinerary_service.get_activities")
def test_get_city_activities_successful_flow(
    mock_get_activities,
    mock_get_geocode,
    mock_city_geocode,
    mock_activities_response
):
    """
    GIVEN a valid city name and radius
    WHEN get_city_activities is called
    THEN it should return an ItineraryResponse with the expected user_id and results.
    """
    # Arrange
    mock_get_geocode.return_value = mock_city_geocode  # e.g. (51.5074, -0.1278)
    mock_get_activities.return_value = mock_activities_response

    user_id = "test_user"
    city_name = "London"
    radius = 10
    limit = 2  # We only want 2 results

    # Act
    response = get_city_activities(user_id, city_name, radius, limit)

    # Assert
    mock_get_geocode.assert_called_once_with(city_name)
    mock_get_activities.assert_called_once_with(
        mock_city_geocode[0],  # lat
        mock_city_geocode[1],  # lon
        radius
    )

    # Check the structure of ItineraryResponse
    assert isinstance(response, ItineraryResponse)
    assert response.user_id == user_id
    assert len(response.results) == 2

    first_activity = response.results[0]
    assert isinstance(first_activity, ItineraryResponseObj)
    assert first_activity.city == city_name
    assert first_activity.activity_id == "ACT_1"
    assert first_activity.price_amount == "25.0"
    assert first_activity.price_currency == "GBP"
    assert first_activity.pictures == "https://example.com/london_eye.jpg"

@patch("src.services.itinerary_service.get_city_geocode")
def test_get_city_activities_cannot_find_geocode(
    mock_get_geocode
):
    """
    GIVEN a city name that cannot be resolved to lat/lon
    WHEN get_city_activities is called
    THEN it should return a dict with an "error" key.
    """
    # Arrange
    mock_get_geocode.return_value = (None, None)

    response = get_city_activities("test_user", "UnknownCity", 5, 2)
    
    # If we return {"error": "..."} it might not be an ItineraryResponse,
    # so check the shape
    assert isinstance(response, dict)
    assert "error" in response
    assert "Could not find geocode" in response["error"]

@patch("src.services.itinerary_service.get_city_geocode")
@patch("src.services.itinerary_service.get_activities")
def test_get_city_activities_limiting_results(
    mock_get_activities,
    mock_get_geocode
):
    """
    GIVEN an API response with more activities than the limit
    WHEN get_city_activities is called with limit=1
    THEN only 1 result should be returned in the final ItineraryResponse.
    """
    mock_get_geocode.return_value = (40.7128, -74.0060)  # Some lat/lon
    mock_get_activities.return_value = {
        "data": [
            {"id": "ACT_1", "name": "Activity One", "price": {"amount": "10.0", "currencyCode": "USD"}, "pictures": []},
            {"id": "ACT_2", "name": "Activity Two", "price": {"amount": "15.0", "currencyCode": "USD"}, "pictures": []}
        ]
    }

    user_id = "limit_user"
    response = get_city_activities(user_id, "SomeCity", 10, limit=1)
    assert len(response.results) == 1  # Only 1 result, respecting limit=1
    assert response.results[0].activity_id == "ACT_1"
    assert response.user_id == user_id
