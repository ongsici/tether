import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def valid_flight_request_payload():
    """
    A valid JSON payload that the /flight endpoint expects.
    """
    return {
        "user_id": "testuser123",
        "flights": {
            "origin_loc_code": "SYD",
            "destination_loc_code": "SIN",
            "departure_date": "2025-03-10",
            "return_date": "2025-03-17",
            "num_passenger": "1"
        }
    }


def mock_flight_response():
    """
    Return a dict that matches the FlightResponse schema structure
    with one outbound and one inbound segment.
    """
    return {
        "user_id": "testuser123",
        "results": [
            {
                "FlightResponse": {
                    "number_of_segments": 2,
                    "flight_id": "some-unique-uuid",
                    "outbound": [
                        {
                            "SegmentResponse": {
                                "num_passengers": 1,
                                "departure_time": "08:00:00",
                                "departure_date": "2025-03-10",
                                "arrival_date": "2025-03-10",
                                "arrival_time": "14:00:00",
                                "duration": "8H",
                                "departure_airport": "SYD",
                                "destination_airport": "SIN",
                                "airline_code": "QF",
                                "flight_number": "81",
                                "unique_id": "QF812025-03-1008:00:00"
                            }
                        }
                    ],
                    "inbound": [
                        {
                            "SegmentResponse": {
                                "num_passengers": 1,
                                "departure_time": "10:00:00",
                                "departure_date": "2025-03-17",
                                "arrival_date": "2025-03-17",
                                "arrival_time": "20:00:00",
                                "duration": "10H",
                                "departure_airport": "SIN",
                                "destination_airport": "SYD",
                                "airline_code": "QF",
                                "flight_number": "82",
                                "unique_id": "QF822025-03-1710:00:00"
                            }
                        }
                    ],
                    "price_per_person": "300"
                }
            }
        ]
    }


@patch("app.get_flights")
def test_post_flight_with_valid_data_returns_200_and_flight_response(
    mock_get_flights, client, valid_flight_request_payload
):
    """
    GIVEN a valid request body
    WHEN the /flight endpoint is called
    THEN it should return status 200 and a well-structured FlightResponse in the JSON body.
    """
    # Arrange
    mock_get_flights.return_value = mock_flight_response()

    # Act
    response = client.post("/flight", json=valid_flight_request_payload)

    # Assert
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["user_id"] == "testuser123"
    assert len(response_json["results"]) == 1
    assert response_json["results"][0]["FlightResponse"]["price_per_person"] == "300"
    # Confirm the service was called with the right arguments
    mock_get_flights.assert_called_once_with(
        "SYD", "SIN", "1", "2025-03-10", "2025-03-17", "testuser123"
    )


@patch("app.get_flights")
def test_post_flight_service_raises_exception_returns_400(
    mock_get_flights, client, valid_flight_request_payload
):
    """
    GIVEN a valid request body
    WHEN the underlying service (get_flights) raises an exception
    THEN the endpoint should catch that exception and return a 400 response with detail info.
    """
    # Simulate an exception in the service
    mock_get_flights.side_effect = Exception("Something went wrong")

    response = client.post("/flight", json=valid_flight_request_payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Something went wrong"
    mock_get_flights.assert_called_once()


@patch("app.get_flights")
def test_post_flight_service_returns_empty_flights_is_still_200(
    mock_get_flights, client, valid_flight_request_payload
):
    """
    GIVEN a valid request body
    WHEN the service returns a FlightResponse with zero results
    THEN the endpoint should respond with 200 and an empty results list.
    """
    mock_get_flights.return_value = {
        "user_id": "testuser123",
        "results": []
    }

    response = client.post("/flight", json=valid_flight_request_payload)
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["user_id"] == "testuser123"
    assert len(response_json["results"]) == 0
    mock_get_flights.assert_called_once()


def test_post_flight_with_missing_required_field_results_in_422(
    client, valid_flight_request_payload
):
    """
    GIVEN a request body missing required fields (e.g. no 'origin_loc_code')
    WHEN the /flight endpoint is called
    THEN FastAPI should respond with a 422 Unprocessable Entity error (validation failure).
    """
    # Remove a required field from the payload
    del valid_flight_request_payload["flights"]["origin_loc_code"]

    response = client.post("/flight", json=valid_flight_request_payload)
    
    # We didn't patch get_flights here because validation
    # is expected to fail before the service is even called.
    assert response.status_code == 422

    # The exact structure of the 422 detail can vary, 
    # but you can at least check the top-level keys or an error substring:
    assert "detail" in response.json()
    assert any("origin_loc_code" in str(err) for err in response.json()["detail"])
