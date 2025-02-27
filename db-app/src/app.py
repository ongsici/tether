from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .services import db_service
from .models.payload_model import UserRequest, FlightSave, FlightUnsave, ItinerarySave, ItineraryUnsave

app = FastAPI(title="Flight and Itinerary API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tether-apim-2.azure-api.net", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# flight endpoints
@app.post("/api/flights/save", status_code=status.HTTP_201_CREATED)
def save_flight(flight: FlightSave):
    try:
        flight_details = flight.flight
        segments = [segment.dict() for segment in flight_details.segments]
        
        return db_service.save_flight(
            user_id=flight.user_id,
            flight_id=flight_details.flight_id,
            total_num_segments=flight_details.total_num_segments,
            price=flight_details.price,
            segments=segments
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/flights/unsave", status_code=status.HTTP_200_OK)
def unsave_flight(flight: FlightUnsave):
    result = db_service.unsave_flight(user_id=flight.user_id, flight_id=flight.flight_id)
    if not result:
        raise HTTPException(status_code=404, detail="Saved flight not found")
    return result

@app.post("/api/flights/get_saved", status_code=status.HTTP_200_OK)
def get_saved_flights(user: UserRequest):
    try:
        return db_service.get_saved_flights(user_id=user.user_id)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# itinerary endpoints
@app.post("/api/itineraries/save", status_code=status.HTTP_201_CREATED)
def save_itinerary(itinerary: ItinerarySave):
    try:
        itinerary_details = itinerary.itinerary

        return db_service.save_itinerary(
            user_id=itinerary.user_id,
            city=itinerary_details.city,
            activity_id=itinerary_details.activity_id,
            activity_name=itinerary_details.activity_name,
            activity_details=itinerary_details.activity_details,
            price_amount=itinerary_details.price_amount,
            price_currency=itinerary_details.price_currency,
            pictures=itinerary_details.pictures
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/itineraries/unsave", status_code=status.HTTP_200_OK)
def unsave_itinerary(itinerary: ItineraryUnsave):
    result = db_service.unsave_itinerary(user_id=itinerary.user_id, activity_id=itinerary.activity_id)
    if not result:
        raise HTTPException(status_code=404, detail="Saved itinerary not found")
    return result

@app.post("/api/itineraries/get_saved", status_code=status.HTTP_200_OK)
def get_saved_itineraries(user: UserRequest):
    try:
        return db_service.get_saved_itineraries(user_id=user.user_id)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/api/itineraries/search", status_code=status.HTTP_200_OK)
# def search_itineraries(search: CitySearch):
#     try:
#         return db_service.search_itineraries(city=search.city)
#     except SQLAlchemyError as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/api/search/flights", status_code=status.HTTP_200_OK)
# def search_flights(search: FlightSearch):
#     try:
#         return db_service.search_flights(
#             departure_airport=search.departure_airport,
#             destination_airport=search.destination_airport
#         )
#     except SQLAlchemyError as e:
#         raise HTTPException(status_code=500, detail=str(e))