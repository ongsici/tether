import pytest
from unittest.mock import patch, MagicMock, call
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from src.services.db_service import save_flight, unsave_flight, get_saved_flights
from src.services.db_service import save_itinerary, unsave_itinerary, get_saved_itineraries
from src.models.db_model import SavedFlight, FlightInfo, FlightSegments, SegmentInfo
from src.models.db_model import SavedItinerary, ItineraryInfo
from src.models.payload_model import SegmentResponse, FlightResponseObj
from src.models.convert_model import FlightSaveDB

@pytest.fixture
def mock_db():
    mock = MagicMock(spec=Session)
    return mock

@pytest.fixture
def mock_flight_data():
    return FlightSaveDB(
        user_id="test_user",
        flight={
            "flight_id": "FL123",
            "total_num_segments": 2,
            "price_per_person": "199.99",
            "total_price": "399.98"
        },
        segments=[{
            "segment_id": "SEG1",
            "airline_code": "AA",
            "flight_code": "123",
            "departure_date": "2025-04-10",
            "departure_time": "10:00",
            "arrival_date": "2025-04-10",
            "arrival_time": "12:00",
            "duration": "2h",
            "departure_airport": "LAX",
            "departure_city": "Los Angeles",
            "destination_airport": "SFO",
            "destination_city": "San Francisco"
        }],
        flight_segments=[{
            "flight_id": "FL123",
            "segment_id": "SEG1",
            "segment_order": 1,
            "bound": "outbound"
        }]
    )

@pytest.fixture
def mock_itinerary_data():
    return {
        "user_id": "test_user",
        "city": "Paris",
        "activity_id": "ACT123",
        "activity_name": "Eiffel Tower Tour",
        "activity_details": "Guided tour of the Eiffel Tower",
        "price_amount": "30.00",
        "price_currency": "EUR",
        "pictures": "https://example.com/eiffel.jpg"
    }


############### FLIGHTS ###############

@patch("src.services.db_service.get_db")
def test_save_new_flight(mock_get_db, mock_db, mock_flight_data):
    """
    GIVEN new flight WHEN save_flight is called
    THEN add flight information and return success message
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # mock new flight
    flight_query = MagicMock()
    flight_query.filter_by.return_value.one_or_none.return_value = None
    
    # configure that user hasn't saved flight yet
    saved_flight_query = MagicMock()
    saved_flight_query.filter_by.return_value.one_or_none.return_value = None
    
    segment_query = MagicMock()
    segment_query.filter_by.return_value.one_or_none.return_value = None

    mock_db.query.side_effect = [
        flight_query,
        segment_query,
        saved_flight_query
    ]
    
    result = save_flight(mock_flight_data)
    
    assert mock_db.add.call_count == 3  # : FlightInfo, SegmentInfo, and SavedFlight
    mock_db.bulk_save_objects.assert_called_once()
    assert mock_db.commit.call_count >= 1
    mock_db.flush.assert_called()
    assert result.user_id == "test_user"
    assert result.status is True
    assert result.message == "Flight saved successfully"

@patch("src.services.db_service.get_db")
def test_save_existing_flight(mock_get_db, mock_db, mock_flight_data):
    """
    GIVEN existing flight WHEN save_flight is called
    THEN increment counter and add to user saved flights
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # mock existing flight
    mock_flight = MagicMock()
    mock_flight.num_users_saved = 1
    
    # configure flight query to return existing flight
    flight_query = MagicMock()
    flight_query.filter_by.return_value.one_or_none.return_value = mock_flight
    
    # configure that user hasn't saved flight yet
    saved_flight_query = MagicMock()
    saved_flight_query.filter_by.return_value.one_or_none.return_value = None
    
    mock_db.query.side_effect = [
        flight_query,
        saved_flight_query
    ]
    
    result = save_flight(mock_flight_data)
    
    assert mock_flight.num_users_saved == 2  # incremented by 1
    assert mock_db.commit.call_count >= 1
    assert result.user_id == "test_user"
    assert result.status is True
    assert result.message == "Flight saved successfully"

@patch("src.services.db_service.get_db")
def test_save_flight_already_saved(mock_get_db, mock_db, mock_flight_data):
    """
    GIVEN flight already saved by user
    WHEN save_flight is called
    THEN return message indicating it's already saved
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # mock existing flight
    mock_flight = MagicMock()
    
    flight_query = MagicMock()
    flight_query.filter_by.return_value.one_or_none.return_value = mock_flight
    
    # configure that user has already saved flight
    mock_saved_flight = MagicMock()
    saved_flight_query = MagicMock()
    saved_flight_query.filter_by.return_value.one_or_none.return_value = mock_saved_flight
    
    mock_db.query.side_effect = [
        flight_query,
        saved_flight_query
    ]
    
    result = save_flight(mock_flight_data)
    
    # flight already saved - should not modify database
    mock_db.add.assert_not_called()
    mock_db.commit.assert_called_once()
    assert result.user_id == "test_user"
    assert result.status is False
    assert result.message == "User already saved flight"

@patch("src.services.db_service.get_db")
def test_unsave_flight_successful(mock_get_db, mock_db):
    """
    GIVEN flight saved by user
    WHEN unsave_flight is called
    THEN remove flight from user saved flights
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    user_id = "test_user"
    flight_id = "FL123"
    
    # mock saved flight
    mock_saved_flight = MagicMock()
    saved_flight_query = MagicMock()
    saved_flight_query.filter_by.return_value.one_or_none.return_value = mock_saved_flight
    
    # mock flight info
    mock_flight_info = MagicMock()
    mock_flight_info.num_users_saved = 1  # only user with flight saved
    flight_info_query = MagicMock()
    flight_info_query.filter_by.return_value.one_or_none.return_value = mock_flight_info
    
    # mock segments query and info
    segment_ids_query = MagicMock()
    segment_ids_query.filter.return_value.all.return_value = [("SEG1",)]
    
    flight_segments_query = MagicMock()
    
    mock_segment_info = MagicMock()
    mock_segment_info.num_flights_saved = 1  # last flight using segment
    segment_info_query = MagicMock()
    segment_info_query.filter_by.return_value.one_or_none.return_value = mock_segment_info
    
    mock_db.query.side_effect = [
        saved_flight_query,
        flight_info_query,
        segment_ids_query,
        flight_segments_query,
        segment_info_query
    ]
    
    result = unsave_flight(user_id, flight_id)
    
    assert mock_db.delete.call_count == 3  # : SavedFlight, FlightInfo, and SegmentInfo
    mock_db.flush.assert_called()
    mock_db.commit.assert_called_once()
    assert result.user_id == user_id
    assert result.status is True
    assert result.message == "Flight successfully removed from saved"

@patch("src.services.db_service.get_db")
def test_unsave_flight_not_saved(mock_get_db, mock_db):
    """
    GIVEN flight not saved by user
    WHEN unsave_flight is called
    THEN return message indicating it's not saved
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    user_id = "test_user"
    flight_id = "FL123"
    
    # configure that user hasn't saved flight
    saved_flight_query = MagicMock()
    saved_flight_query.filter_by.return_value.one_or_none.return_value = None
    mock_db.query.return_value = saved_flight_query
    
    result = unsave_flight(user_id, flight_id)
    
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_called_once()
    assert result.user_id == user_id
    assert result.status is False
    assert result.message == "User does not have this flight saved"

# @patch("src.services.db_service.get_db")
# def test_get_saved_flights(mock_get_db, mock_db):
#     """
#     GIVEN user with saved flights
#     WHEN get_saved_flights is called
#     THEN return saved flights information
#     """
#     mock_get_db.return_value.__next__.return_value = mock_db
#     user_id = "test_user"
    
#     # mock saved flight
#     mock_saved_flight = MagicMock()
#     mock_saved_flight.flight_id = "FL123"
#     saved_flights_query = MagicMock()
#     saved_flights_query.filter.return_value.all.return_value = [mock_saved_flight]
    
#     # mock flight and segment info/query
#     mock_flight_info = MagicMock()
#     mock_flight_info.flight_id = "FL123"
#     mock_flight_info.total_num_segments = 2
#     mock_flight_info.price_per_person = "199.99"
#     mock_flight_info.total_price = "399.98"
#     flight_info_query = MagicMock()
#     flight_info_query.filter.return_value.one_or_none.return_value = mock_flight_info
    
#     mock_out_segment = MagicMock()
#     mock_out_segment.segment_id = "SEG1"
#     mock_out_segment.airline_code = "AA"
#     mock_out_segment.flight_code = "123"
#     mock_out_segment.departure_date = "2025-04-10"
#     mock_out_segment.departure_time = "10:00"
#     mock_out_segment.arrival_date = "2025-04-10"
#     mock_out_segment.arrival_time = "12:00"
#     mock_out_segment.duration = "2h"
#     mock_out_segment.departure_airport = "LAX"
#     mock_out_segment.departure_city = "Los Angeles"
#     mock_out_segment.destination_airport = "SFO"
#     mock_out_segment.destination_city = "San Francisco"
    
#     # mock outbound query
#     outbound_query = MagicMock()
#     outbound_join = MagicMock()
#     outbound_filter1 = MagicMock()
#     outbound_filter2 = MagicMock()
#     outbound_query.join.return_value = outbound_join
#     outbound_join.filter.return_value = outbound_filter1
#     outbound_filter1.filter.return_value = outbound_filter2
#     outbound_filter2.order_by.return_value.all.return_value = [(mock_out_segment, 1)]
    
#     # mock inbound query
#     inbound_query = MagicMock()
#     inbound_join = MagicMock()
#     inbound_filter1 = MagicMock()
#     inbound_filter2 = MagicMock()
#     inbound_join.filter.return_value = inbound_filter1
#     inbound_filter1.filter.return_value = inbound_filter2
#     inbound_filter2.order_by.return_value.all.return_value = []  # no inbound segments
    
#     mock_db.query.side_effect = [
#         saved_flights_query,
#         flight_info_query,
#         outbound_query,
#         inbound_query
#     ]
    
#     response = get_saved_flights(user_id)
    
#     assert response.user_id == user_id
#     assert len(response.flights) == 1

#     flight_response_wrapper = response.flights[0]
#     flight = flight_response_wrapper.FlightResponse

#     assert flight.flight_id == "FL123"
#     assert flight.number_of_segments == 2
#     assert flight.price_per_person == "199.99"
#     assert flight.total_price == "399.98"

#     assert len(flight.outbound) == 1
#     assert len(flight.inbound) == 0

#     segment = flight.outbound[0].SegmentResponse

#     assert segment.departure_time == "10:00"
#     assert segment.departure_date == "2025-04-10"
#     assert segment.arrival_date == "2025-04-10"
#     assert segment.arrival_time == "12:00"
#     assert segment.departure_airport == "LAX"
#     assert segment.destination_airport == "SFO"
#     assert segment.unique_id == "SEG1"
#     assert segment.airline_code == "AA"
#     assert segment.flight_number == "123"

#     mock_db.commit.assert_called_once()


############### ITINERARY ###############

@patch("src.services.db_service.get_db")
def test_save_new_itinerary(mock_get_db, mock_db, mock_itinerary_data):
    """
    GIVEN new itinerary WHEN save_itinerary is called
    THEN add itinerary information and return success message
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # mock new itinerary
    itinerary_query = MagicMock()
    itinerary_query.filter_by.return_value.one_or_none.return_value = None
    
    # configure that user hasn't saved itinerary yet
    saved_itinerary_query = MagicMock()
    saved_itinerary_query.filter_by.return_value.one_or_none.return_value = None
    
    mock_db.query.side_effect = [
        itinerary_query,
        saved_itinerary_query
    ]
    
    result = save_itinerary(**mock_itinerary_data)
    
    assert mock_db.add.call_count == 2  # : ItineraryInfo and SavedItinerary
    mock_db.commit.assert_called_once()
    assert result.user_id == "test_user"
    assert result.status is True
    assert result.message == "Itinerary saved successfully"

@patch("src.services.db_service.get_db")
def test_save_existing_itinerary(mock_get_db, mock_db, mock_itinerary_data):
    """
    GIVEN existing itinerary WHEN save_itinerary is called
    THEN increment counter and add to user saved itineraries
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # mock existing itinerary
    mock_itinerary = MagicMock()
    mock_itinerary.num_users_saved = 1
    itinerary_query = MagicMock()
    itinerary_query.filter_by.return_value.one_or_none.return_value = mock_itinerary
    
    # configure that user hasn't saved itinerary yet
    saved_itinerary_query = MagicMock()
    saved_itinerary_query.filter_by.return_value.one_or_none.return_value = None
    
    mock_db.query.side_effect = [
        itinerary_query,
        saved_itinerary_query
    ]
    
    result = save_itinerary(**mock_itinerary_data)
    
    assert mock_itinerary.num_users_saved == 2  # incremented by 1
    assert mock_db.add.call_count == 1  # only for SavedItinerary
    mock_db.commit.assert_called_once()
    assert result.user_id == "test_user"
    assert result.status is True
    assert result.message == "Itinerary saved successfully"

@patch("src.services.db_service.get_db")
def test_save_itinerary_already_saved(mock_get_db, mock_db, mock_itinerary_data):
    """
    GIVEN itinerary already saved by user
    WHEN save_itinerary is called
    THEN return message indicating it's already saved
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    
    # mock existing itinerary
    mock_itinerary = MagicMock()
    itinerary_query = MagicMock()
    itinerary_query.filter_by.return_value.one_or_none.return_value = mock_itinerary
    
    # configure that user has already saved itinerary
    mock_saved_itinerary = MagicMock()
    saved_itinerary_query = MagicMock()
    saved_itinerary_query.filter_by.return_value.one_or_none.return_value = mock_saved_itinerary
    
    mock_db.query.side_effect = [
        itinerary_query,
        saved_itinerary_query
    ]
    
    result = save_itinerary(**mock_itinerary_data)
    
    # itinerary already saved - should not modify database
    mock_db.add.assert_not_called()
    mock_db.commit.assert_called_once()
    assert result.user_id == "test_user"
    assert result.status is False
    assert result.message == "User already saved itinerary"

@patch("src.services.db_service.get_db")
def test_unsave_itinerary_successful(mock_get_db, mock_db):
    """
    GIVEN itinerary saved by user
    WHEN unsave_itinerary is called
    THEN remove itinerary from user saved itineraries
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    user_id = "test_user"
    activity_id = "ACT123"
    
    # mock saved itinerary
    mock_saved_itinerary = MagicMock()
    saved_itinerary_query = MagicMock()
    saved_itinerary_query.filter_by.return_value.one_or_none.return_value = mock_saved_itinerary
    
    # mock itinerary info
    mock_itinerary_info = MagicMock()
    mock_itinerary_info.num_users_saved = 1  # only user with itinerary saved
    itinerary_info_query = MagicMock()
    itinerary_info_query.filter_by.return_value.one_or_none.return_value = mock_itinerary_info
    
    mock_db.query.side_effect = [
        saved_itinerary_query,
        itinerary_info_query
    ]
    
    result = unsave_itinerary(user_id, activity_id)
    
    assert mock_db.delete.call_count == 2  # : SavedItinerary and ItineraryInfo
    mock_db.flush.assert_called()
    mock_db.commit.assert_called_once()
    assert result.user_id == user_id
    assert result.status is True
    assert result.message == "Itinerary removed from saved"

@patch("src.services.db_service.get_db")
def test_unsave_itinerary_not_saved(mock_get_db, mock_db):
    """
    GIVEN itinerary not saved by user
    WHEN unsave_itinerary is called
    THEN return message indicating it's not saved
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    user_id = "test_user"
    activity_id = "ACT123"
    
    # configure that user hasn't saved itinerary
    saved_itinerary_query = MagicMock()
    saved_itinerary_query.filter_by.return_value.one_or_none.return_value = None
    mock_db.query.return_value = saved_itinerary_query
    
    result = unsave_itinerary(user_id, activity_id)
    
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_called_once()
    assert result.user_id == user_id
    assert result.status is False
    assert result.message == "User does not have this itinerary saved"

@patch("src.services.db_service.get_db")
def test_get_saved_itineraries(mock_get_db, mock_db):
    """
    GIVEN user with saved itineraries
    WHEN get_saved_itineraries is called
    THEN return saved itineraries information
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    user_id = "test_user"
    
    # mock itinerary
    mock_itinerary = MagicMock()
    mock_itinerary.city = "Paris"
    mock_itinerary.activity_id = "ACT123"
    mock_itinerary.activity_name = "Eiffel Tower Tour"
    mock_itinerary.activity_details = "Guided tour of the Eiffel Tower"
    mock_itinerary.price_amount = "30.00"
    mock_itinerary.price_currency = "EUR"
    mock_itinerary.pictures = "https://example.com/eiffel.jpg"
    
    # mock query for itineraries
    join_query = MagicMock()
    filter_query = MagicMock()
    join_query.filter.return_value = filter_query
    filter_query.all.return_value = [mock_itinerary]
    
    itinerary_query = MagicMock()
    itinerary_query.join.return_value = join_query
    mock_db.query.return_value = itinerary_query
    
    response = get_saved_itineraries(user_id)
    
    assert response.user_id == user_id
    assert len(response.itinerary) == 1
    itinerary = response.itinerary[0]
    assert itinerary.city == "Paris"
    assert itinerary.activity_id == "ACT123"
    assert itinerary.activity_name == "Eiffel Tower Tour"
    assert itinerary.price_amount == "30.00"
    assert itinerary.price_currency == "EUR"
    mock_db.commit.assert_called_once()

@patch("src.services.db_service.get_db")
def test_db_operation_decorator_handles_exceptions(mock_get_db, mock_db):
    """
    GIVEN database operation that raises an exception
    WHEN decorated with db_operation
    THEN handle exception properly
    """
    mock_get_db.return_value.__next__.return_value = mock_db
    mock_db.query.side_effect = SQLAlchemyError("Database error")
    
    with pytest.raises(SQLAlchemyError):
        get_saved_flights("test_user")
    
    # verify proper cleanup
    mock_db.rollback.assert_called_once()
    mock_db.close.assert_called_once()
    mock_db.commit.assert_not_called()