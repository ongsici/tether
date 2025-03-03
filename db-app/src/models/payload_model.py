from pydantic import BaseModel
from typing import List


# model for request validation
class UserRequest(BaseModel):
    user_id: str


##### FLIGHTS #####

# front-end / API response
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

class SegmentResponseWrapper(BaseModel):
    SegmentResponse: SegmentResponse

class FlightResponseObj(BaseModel):
    number_of_segments: int
    flight_id: str
    outbound: List[SegmentResponseWrapper] = []
    inbound: List[SegmentResponseWrapper] = []
    price_per_person: str

class FlightResponseObjWrapper(BaseModel):
    FlightResponse: FlightResponseObj

# save / view responses
class FlightSaveRequest(BaseModel):
    user_id: str
    flights: FlightResponseObjWrapper

class FlightViewResponse(BaseModel):
    user_id: str
    flights: List[FlightResponseObjWrapper]

# unsave response
class FlightUnsaveRequest(BaseModel):
    user_id: str
    flight_id: str


##### ITINERARY #####

class ItineraryDetails(BaseModel):
    city: str
    activity_id: str
    activity_name: str
    activity_details: str
    price_amount: str
    price_currency: str
    pictures: str

class ItinerarySaveRequest(BaseModel):
    user_id: str
    itinerary: ItineraryDetails

class ItineraryViewResponse(BaseModel):
    user_id: str
    itinerary: List[ItineraryDetails]

class ItineraryUnsaveRequest(BaseModel):
    user_id: str
    activity_id: str
