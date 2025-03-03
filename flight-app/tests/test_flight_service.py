import pytest
from unittest.mock import patch
from src.services.flight_service import get_flights


@pytest.fixture
def single_round_trip_mock_data():
    """
    Simple mock data for a single round-trip flight 
    from SYD -> SIN -> SYD with a base price of 300.
    """
    return {
        "data": [
            {
                "price": {"base": "300"},
                "itineraries": [
                    {
                        "segments": [
                            {
                                "departure": {
                                    "iataCode": "SYD",
                                    "at": "2025-03-10T08:00:00"
                                },
                                "arrival": {
                                    "iataCode": "SIN",
                                    "at": "2025-03-10T14:00:00"
                                },
                                "carrierCode": "QF",
                                "number": "81",
                                "duration": "PT8H"
                            }
                        ]
                    },
                    {
                        "segments": [
                            {
                                "departure": {
                                    "iataCode": "SIN",
                                    "at": "2025-03-17T10:00:00"
                                },
                                "arrival": {
                                    "iataCode": "SYD",
                                    "at": "2025-03-17T20:00:00"
                                },
                                "carrierCode": "QF",
                                "number": "82",
                                "duration": "PT8H"
                            }
                        ]
                    }
                ]
            }
        ]
    }


@patch("src.services.flight_service.get_flight_data")
def test_call_get_flights_with_valid_data_gives_correct_response_structure(
    mock_get_flight_data, 
    single_round_trip_mock_data
):
    """
    GIVEN a valid call to get_flights with a single round-trip flight returned
    WHEN the function is invoked
    THEN it should return a FlightResponse with the correct user_id, number_of_segments, 
         and properly constructed outbound/inbound segments.
    """
    mock_get_flight_data.return_value = single_round_trip_mock_data

    origin = "SYD"
    destination = "SIN"
    num_passenger = "1"
    departure_date = "2025-03-10"
    return_date = "2025-03-17"
    user_id = "testuser123"

    response = get_flights(
        origin,
        destination,
        num_passenger,
        departure_date,
        return_date,
        user_id
    )

    mock_get_flight_data.assert_called_once_with(
        origin, destination, num_passenger, departure_date, return_date
    )

    assert response.user_id == user_id
    assert len(response.results) == 1

    flight_obj = response.results[0].FlightResponse
    assert flight_obj.price_per_person == "300"
    assert flight_obj.number_of_segments == 2
    assert len(flight_obj.outbound) == 1
    assert len(flight_obj.inbound) == 1

    outbound_segment = flight_obj.outbound[0].SegmentResponse
    assert outbound_segment.departure_airport == "SYD"
    assert outbound_segment.destination_airport == "SIN"
    assert outbound_segment.duration == "8H"
    assert outbound_segment.num_passengers == int(num_passenger)

    inbound_segment = flight_obj.inbound[0].SegmentResponse
    assert inbound_segment.departure_airport == "SIN"
    assert inbound_segment.destination_airport == "SYD"
    assert inbound_segment.duration == "8H"


def test_call_get_flights_with_no_data_returns_empty_results():
    """
    GIVEN a scenario where the Amadeus API returns an empty 'data' list
    WHEN get_flights is called
    THEN the resulting FlightResponse should have 0 flights in 'results'.
    """
    with patch("src.services.flight_service.get_flight_data") as mock_get_flight_data:
        mock_get_flight_data.return_value = {"data": []}

        response = get_flights(
            origin_loc_code="SYD",
            destination_loc_code="SIN",
            num_passenger="1",
            departure_date="2025-03-10",
            return_date="2025-03-17",
            user_id="testuser123"
        )

        mock_get_flight_data.assert_called_once()
        assert response.user_id == "testuser123"
        assert len(response.results) == 0


@patch("src.services.flight_service.get_flight_data")
def test_call_get_flights_with_multiple_itineraries_returns_correct_flights(
    mock_get_flight_data
):
    """
    GIVEN a scenario with multiple flight 'data' entries and each entry having 2 itineraries
    WHEN get_flights is called
    THEN each flight entry should be parsed into a FlightResponseObj, 
         reflecting correct price, segment counts, etc.
    """
    mock_data = {
        "data": [
            {
                "price": {"base": "500"},
                "itineraries": [
                    {
                        "segments": [
                            {
                                "departure": {"iataCode": "SYD", "at": "2025-04-01T09:00:00"},
                                "arrival": {"iataCode": "LAX", "at": "2025-04-01T21:00:00"},
                                "carrierCode": "QF",
                                "number": "11",
                                "duration": "PT12H"
                            }
                        ]
                    },
                    {
                        "segments": [
                            {
                                "departure": {"iataCode": "LAX", "at": "2025-04-10T15:00:00"},
                                "arrival": {"iataCode": "SYD", "at": "2025-04-11T01:00:00"},
                                "carrierCode": "QF",
                                "number": "12",
                                "duration": "PT14H"
                            }
                        ]
                    }
                ]
            },
            {
                "price": {"base": 750},
                "itineraries": [
                    {
                        "segments": [
                            {
                                "departure": {"iataCode": "SYD", "at": "2025-04-01T10:00:00"},
                                "arrival": {"iataCode": "LAX", "at": "2025-04-01T22:00:00"},
                                "carrierCode": "UA",
                                "number": "840",
                                "duration": "PT12H"
                            }
                        ]
                    },
                    {
                        "segments": [
                            {
                                "departure": {"iataCode": "LAX", "at": "2025-04-10T08:00:00"},
                                "arrival": {"iataCode": "SYD", "at": "2025-04-11T00:00:00"},
                                "carrierCode": "UA",
                                "number": "839",
                                "duration": "PT14H"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    mock_get_flight_data.return_value = mock_data

    user_id = "testuser999"
    response = get_flights("SYD", "LAX", "1", "2025-04-01", "2025-04-10", user_id)

    assert response.user_id == user_id
    assert len(response.results) == 2

    flight1 = response.results[0].FlightResponse
    assert flight1.price_per_person == "500"
    assert flight1.number_of_segments == 2
    assert len(flight1.outbound) == 1
    assert len(flight1.inbound) == 1

    flight2 = response.results[1].FlightResponse
    assert flight2.price_per_person == "750"
    assert flight2.number_of_segments == 2


@patch("src.services.flight_service.get_flight_data")
def test_call_get_flights_when_get_flight_data_raises_exception_propagates_error(
    mock_get_flight_data
):
    """
    GIVEN get_flight_data raises an exception (e.g. network error or invalid token)
    WHEN get_flights is called
    THEN the function should let the exception propagate.
    """
    mock_get_flight_data.side_effect = Exception("Network error / invalid token")

    with pytest.raises(Exception) as excinfo:
        get_flights("SYD", "SIN", "2", "2025-03-10", "2025-03-17", "exception_user")

    assert "Network error / invalid token" in str(excinfo.value)
    mock_get_flight_data.assert_called_once()


@patch("src.services.flight_service.get_flight_data")
def test_call_get_flights_ignores_itineraries_with_more_than_three_segments(
    mock_get_flight_data
):
    """
    GIVEN an itinerary that has more than three segments
    WHEN get_flights is called
    THEN that itinerary should be skipped (per the logic `if len(itinerary['segments']) > 3: continue`).
    """
    mock_data = {
        "data": [
            {
                "price": {"base": 1000},
                "itineraries": [
                    {  # Outbound with 4 segments => should be skipped entirely
                        "segments": [
                            {"carrierCode": "AB", "number": "123", "duration": "PT2H",
                             "departure": {"iataCode": "XXX", "at": "2025-01-01T01:00:00"},
                             "arrival": {"iataCode": "YYY", "at": "2025-01-01T03:00:00"}},
                            {"carrierCode": "AB", "number": "456", "duration": "PT2H",
                             "departure": {"iataCode": "YYY", "at": "2025-01-01T04:00:00"},
                             "arrival": {"iataCode": "ZZZ", "at": "2025-01-01T06:00:00"}},
                            {"carrierCode": "AB", "number": "789", "duration": "PT2H",
                             "departure": {"iataCode": "ZZZ", "at": "2025-01-01T07:00:00"},
                             "arrival": {"iataCode": "WWW", "at": "2025-01-01T09:00:00"}},
                            {"carrierCode": "AB", "number": "101", "duration": "PT2H",
                             "departure": {"iataCode": "WWW", "at": "2025-01-01T10:00:00"},
                             "arrival": {"iataCode": "CCC", "at": "2025-01-01T12:00:00"}}
                        ]
                    },
                    {  # Inbound with 1 segment => but outbound has 4, so entire flight is effectively skipped
                        "segments": [
                            {
                                "departure": {"iataCode": "CCC", "at": "2025-01-05T06:00:00"},
                                "arrival": {"iataCode": "XXX", "at": "2025-01-05T16:00:00"},
                                "carrierCode": "AB",
                                "number": "202",
                                "duration": "PT10H"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    mock_get_flight_data.return_value = mock_data

    response = get_flights("XXX", "CCC", "1", "2025-01-01", "2025-01-05", "4_segments_test")
    mock_get_flight_data.assert_called_once()

    assert len(response.results) == 0, "Itinerary with 4 segments should be ignored completely."
