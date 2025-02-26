from pydantic import BaseModel
from typing import List

# request model for endpoint
class FlightRequestObj(BaseModel):
    origin_loc_code: str
    destination_loc_code: str
    num_passenger: str
    departure_date: str
    return_date: str

class FlightRequest(BaseModel):
    user_id: str
    flights: FlightRequestObj

class SegmentResponse(BaseModel):
    num_passengers: int
    departure_time: str
    departure_date: str
    arrival_date: str
    arrival_time: str
    duration: str
    departure_airport: str
    destination_airport: str
    airline_code: str
    flight_number: str
    segment_id: str


class FlightResponseObj(BaseModel):
    number_of_segments: int
    flight_id: str
    segment_info: List[SegmentResponse] = []
    price_per_person: str


class FlightResponse(BaseModel):
    user_id: str
    results: List[FlightResponseObj] = []

