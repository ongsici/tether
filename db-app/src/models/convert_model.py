from pydantic import BaseModel
from typing import List
from ..models.payload_model import FlightSaveRequest


class SegmentData(BaseModel):
    segment_id: str
    airline_code: str
    flight_code: str
    departure_date: str
    departure_time: str
    arrival_date: str
    arrival_time: str
    duration: str
    departure_airport: str
    destination_airport: str

class FlightData(BaseModel):
    flight_id: str
    total_num_segments: int
    price: str

class FlightSegmentData(BaseModel):
    flight_id: str
    segment_id: str
    segment_order: int
    bound: str

class FlightSaveDB(BaseModel):
    user_id: str
    flight: FlightData
    segments: List[SegmentData]
    flight_segments: List[FlightSegmentData]


# convert FlightSaveRequest to FlightSaveDB
def transform_flight_save(flight_request: FlightSaveRequest) -> dict:
    flight_info = flight_request.flights.FlightResponse
    
    # saving segments info
    db_segments = []
    for segment_wrapper in flight_info.outbound + flight_info.inbound:
        s = segment_wrapper.SegmentResponse
        db_segments.append(SegmentData(
            segment_id = s.unique_id,
            airline_code = s.airline_code,
            flight_code = s.flight_number,
            departure_date = s.departure_date,
            departure_time = s.departure_time,
            arrival_date = s.arrival_date,
            arrival_time = s.arrival_time,
            duration = s.duration,
            departure_airport = s.departure_airport,
            destination_airport = s.destination_airport
        ))
    
    # saving flight relation with segments
    db_flight_segments = []
    idx = 1
    for outbound_wrapper in flight_info.outbound:
        o = outbound_wrapper.SegmentResponse
        db_flight_segments.append(FlightSegmentData(
            flight_id = flight_info.flight_id,
            segment_id = o.unique_id,
            segment_order = idx,
            bound = 'outbound'
        ))
        idx += 1
    
    idx = 1
    for inbound_wrapper in flight_info.inbound:
        i = inbound_wrapper.SegmentResponse
        db_flight_segments.append(FlightSegmentData(
            flight_id = flight_info.flight_id,
            segment_id = i.unique_id,
            segment_order = idx,
            bound = 'inbound'
        ))
        idx += 1

    # saving other flight data    
    flight_details = FlightData(
        flight_id = flight_info.flight_id,
        total_num_segments = flight_info.number_of_segments,
        price = flight_info.price_per_person,
    )

    db_model = FlightSaveDB(
        user_id = flight_request.user_id,
        flight = flight_details,
        segments = db_segments,
        flight_segments = db_flight_segments
    )

    return db_model


# convert SavedFlight to printing format (FlightViewResponse)

