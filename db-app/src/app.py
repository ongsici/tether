from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel

from .services.db_service import get_db_session
from .services import db_service
from .models.db_model import Base, User, SavedFlight, FlightInfo, SegmentInfo, SavedItinerary, ItineraryInfo

# models for request validation
class UserCreate(BaseModel):
    user_id: str
    user_details: Optional[str] = None

class UserGet(BaseModel):
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

class FlightSave(BaseModel):
    user_id: str
    flight_id: str
    total_num_segments: int
    price: str
    segments: List[SegmentData]

class FlightAction(BaseModel):
    user_id: str
    flight_id: str

class ItinerarySave(BaseModel):
    user_id: str
    city: str
    activity_id: str
    activity_name: str
    activity_details: str
    price_amount: str
    price_currency: str
    pictures: Optional[List[str]] = []

class ItineraryAction(BaseModel):
    user_id: str
    activity_id: str

class CitySearch(BaseModel):
    city: str

class FlightSearch(BaseModel):
    departure_airport: str
    destination_airport: str

app = FastAPI(title="Flight and Itinerary API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# user endpoints
@app.post("/api/user/create", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        return db_service.create_user(user_id=user.user_id, user_details=user.user_details)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/get", status_code=status.HTTP_200_OK)
def get_user(user: UserGet):
    db_user = db_service.get_user(user_id=user.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# flight endpoints
@app.post("/api/flights/save", status_code=status.HTTP_201_CREATED)
def save_flight(flight: FlightSave):
    try:
        segments = [segment.dict() for segment in flight.segments]
        
        return db_service.save_flight(
            user_id=flight.user_id,
            flight_id=flight.flight_id,
            total_num_segments=flight.total_num_segments,
            price=flight.price,
            segments=segments
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/flights/unsave", status_code=status.HTTP_200_OK)
def unsave_flight(flight: FlightAction):
    result = db_service.unsave_flight(user_id=flight.user_id, flight_id=flight.flight_id)
    if not result:
        raise HTTPException(status_code=404, detail="Saved flight not found")
    return result

@app.post("/api/flights/get_saved", status_code=status.HTTP_200_OK)
def get_saved_flights(user: UserGet):
    try:
        return db_service.get_saved_flights(user_id=user.user_id)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# itinerary endpoints
@app.post("/api/itineraries/save", status_code=status.HTTP_201_CREATED)
def save_itinerary(itinerary: ItinerarySave):
    try:
        return db_service.save_itinerary(
            user_id=itinerary.user_id,
            city=itinerary.city,
            activity_id=itinerary.activity_id,
            activity_name=itinerary.activity_name,
            activity_details=itinerary.activity_details,
            price_amount=itinerary.price_amount,
            price_currency=itinerary.price_currency,
            pictures=itinerary.pictures
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/itineraries/unsave", status_code=status.HTTP_200_OK)
def unsave_itinerary(itinerary: ItineraryAction):
    result = db_service.unsave_itinerary(user_id=itinerary.user_id, activity_id=itinerary.activity_id)
    if not result:
        raise HTTPException(status_code=404, detail="Saved itinerary not found")
    return result

@app.post("/api/itineraries/get_saved", status_code=status.HTTP_200_OK)
def get_saved_itineraries(user: UserGet):
    try:
        return db_service.get_saved_itineraries(user_id=user.user_id)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/itineraries/search", status_code=status.HTTP_200_OK)
def search_itineraries(search: CitySearch):
    try:
        return db_service.search_itineraries(city=search.city)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search/flights", status_code=status.HTTP_200_OK)
def search_flights(search: FlightSearch):
    try:
        return db_service.search_flights(
            departure_airport=search.departure_airport,
            destination_airport=search.destination_airport
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)