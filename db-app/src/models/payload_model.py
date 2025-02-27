from pydantic import BaseModel
from typing import List


# models for request validation
class UserRequest(BaseModel):
    user_id: str

class SegmentData(BaseModel):
    index: int
    segment_id: int
    airline_code: str
    flight_code: str
    departure_date: str
    departure_time: str
    arrival_date: str
    arrival_time: str
    duration: str
    departure_airport: str
    destination_airport: str

class FlightDetails(BaseModel):
    flight_id: str
    total_num_segments: int
    price: str
    segments: List[SegmentData]

class FlightSave(BaseModel):
    user_id: str
    flight: FlightDetails

class FlightUnsave(BaseModel):
    user_id: str
    flight_id: str

class ItineraryDetails(BaseModel):
    city: str
    activity_id: str
    activity_name: str
    activity_details: str
    price_amount: str
    price_currency: str
    pictures: str

class ItinerarySave(BaseModel):
    user_id: str
    itinerary: ItineraryDetails

class ItineraryUnsave(BaseModel):
    user_id: str
    activity_id: str

class CitySearch(BaseModel):
    city: str

class FlightSearch(BaseModel):
    departure_airport: str
    destination_airport: str