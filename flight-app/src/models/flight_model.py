from pydantic import BaseModel
from typing import List, Optional

# request model for endpoint
class FlightRequest(BaseModel):
    origin_loc_code: str
    destination_loc_code: str
    num_passenger: str
    departure_date: str
    return_date: str = None

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
    unique_id: str

class FlightResponse(BaseModel):
    number_of_segments: int
    segment_info: List[SegmentResponse] = []
    price_per_person = str
