from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel
import json
from .models.db_model import Base, User, SavedFlight, FlightInfo, SegmentInfo, SavedItinerary, ItineraryInfo

# Pydantic models for request validation
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

# Configure database
DATABASE_URL = "sqlite:///flight_itinerary.db"  # Change this to your database URL
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# Create FastAPI instance
app = FastAPI(title="Flight and Itinerary API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User endpoints
@app.post("/api/user/create", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(user_id=user.user_id, user_details=user.user_details or "")
        db.add(db_user)
        db.commit()
        return {"message": "User created successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/get", status_code=status.HTTP_200_OK)
def get_user(user: UserGet, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(user_id=user.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": db_user.user_id, "user_details": db_user.user_details}

# Flight endpoints
@app.post("/api/flights/save", status_code=status.HTTP_201_CREATED)
def save_flight(flight: FlightSave, db: Session = Depends(get_db)):
    try:
        # Check if flight exists, if not create it
        db_flight = db.query(FlightInfo).filter_by(flight_id=flight.flight_id).first()
        if not db_flight:
            db_flight = FlightInfo(
                flight_id=flight.flight_id,
                total_num_segments=flight.total_num_segments,
                price=flight.price,
                num_users_saved=1
            )
            db.add(db_flight)
            
            # Add segment information
            for segment in flight.segments:
                seg = SegmentInfo(
                    flight_id=flight.flight_id,
                    index=segment.index,
                    segment_id=segment.segment_id,
                    airline_code=segment.airline_code,
                    flight_code=segment.flight_code,
                    departure_date=segment.departure_date,
                    departure_time=segment.departure_time,
                    arrival_date=segment.arrival_date,
                    arrival_time=segment.arrival_time,
                    duration=segment.duration,
                    departure_airport=segment.departure_airport,
                    destination_airport=segment.destination_airport
                )
                db.add(seg)
        else:
            # Increment number of users who saved this flight
            db_flight.num_users_saved += 1
        
        # Create saved flight entry
        saved_flight = SavedFlight(user_id=flight.user_id, flight_id=flight.flight_id)
        db.add(saved_flight)
        db.commit()
        return {"message": "Flight saved successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/flights/unsave", status_code=status.HTTP_200_OK)
def unsave_flight(flight: FlightAction, db: Session = Depends(get_db)):
    saved_flight = db.query(SavedFlight).filter_by(
        user_id=flight.user_id, 
        flight_id=flight.flight_id
    ).first()
    
    if not saved_flight:
        raise HTTPException(status_code=404, detail="Saved flight not found")
    
    try:
        flight_info = db.query(FlightInfo).filter_by(flight_id=flight.flight_id).first()
        if flight_info and flight_info.num_users_saved > 0:
            flight_info.num_users_saved -= 1
        
        db.delete(saved_flight)
        db.commit()
        return {"message": "Flight removed from saved"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/flights/get_saved", status_code=status.HTTP_200_OK)
def get_saved_flights(user: UserGet, db: Session = Depends(get_db)):
    try:
        saved_flights = db.query(SavedFlight).filter_by(user_id=user.user_id).all()
        flight_ids = [sf.flight_id for sf in saved_flights]
        
        flights = []
        for flight_id in flight_ids:
            flight_info = db.query(FlightInfo).filter_by(flight_id=flight_id).first()
            if flight_info:
                segments = db.query(SegmentInfo).filter_by(flight_id=flight_id).all()
                segments_data = [{
                    'index': seg.index,
                    'segment_id': seg.segment_id,
                    'airline_code': seg.airline_code,
                    'flight_code': seg.flight_code,
                    'departure_date': seg.departure_date,
                    'departure_time': seg.departure_time,
                    'arrival_date': seg.arrival_date,
                    'arrival_time': seg.arrival_time,
                    'duration': seg.duration,
                    'departure_airport': seg.departure_airport,
                    'destination_airport': seg.destination_airport
                } for seg in segments]
                
                flights.append({
                    'flight_id': flight_info.flight_id,
                    'total_num_segments': flight_info.total_num_segments,
                    'price': flight_info.price,
                    'segments': segments_data
                })
        
        return {"flights": flights}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Itinerary endpoints
@app.post("/api/itineraries/save", status_code=status.HTTP_201_CREATED)
def save_itinerary(itinerary: ItinerarySave, db: Session = Depends(get_db)):
    try:
        # Check if itinerary exists, if not create it
        db_itinerary = db.query(ItineraryInfo).filter_by(activity_id=itinerary.activity_id).first()
        if not db_itinerary:
            db_itinerary = ItineraryInfo(
                city=itinerary.city,
                activity_id=itinerary.activity_id,
                activity_name=itinerary.activity_name,
                activity_details=itinerary.activity_details,
                price_amount=itinerary.price_amount,
                price_currency=itinerary.price_currency,
                pictures=json.dumps(itinerary.pictures),
                num_users_saved=1
            )
            db.add(db_itinerary)
        else:
            # Increment number of users who saved this itinerary
            db_itinerary.num_users_saved += 1
        
        # Create saved itinerary entry
        saved_itinerary = SavedItinerary(user_id=itinerary.user_id, activity_id=itinerary.activity_id)
        db.add(saved_itinerary)
        db.commit()
        return {"message": "Itinerary saved successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/itineraries/unsave", status_code=status.HTTP_200_OK)
def unsave_itinerary(itinerary: ItineraryAction, db: Session = Depends(get_db)):
    saved_itinerary = db.query(SavedItinerary).filter_by(
        user_id=itinerary.user_id, 
        activity_id=itinerary.activity_id
    ).first()
    
    if not saved_itinerary:
        raise HTTPException(status_code=404, detail="Saved itinerary not found")
    
    try:
        itinerary_info = db.query(ItineraryInfo).filter_by(activity_id=itinerary.activity_id).first()
        if itinerary_info and itinerary_info.num_users_saved > 0:
            itinerary_info.num_users_saved -= 1
        
        db.delete(saved_itinerary)
        db.commit()
        return {"message": "Itinerary removed from saved"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/itineraries/get_saved", status_code=status.HTTP_200_OK)
def get_saved_itineraries(user: UserGet, db: Session = Depends(get_db)):
    try:
        saved_itineraries = db.query(SavedItinerary).filter_by(user_id=user.user_id).all()
        activity_ids = [si.activity_id for si in saved_itineraries]
        
        itineraries = []
        for activity_id in activity_ids:
            itinerary_info = db.query(ItineraryInfo).filter_by(activity_id=activity_id).first()
            if itinerary_info:
                itineraries.append({
                    'city': itinerary_info.city,
                    'activity_id': itinerary_info.activity_id,
                    'activity_name': itinerary_info.activity_name,
                    'activity_details': itinerary_info.activity_details,
                    'price_amount': itinerary_info.price_amount,
                    'price_currency': itinerary_info.price_currency,
                    'pictures': json.loads(itinerary_info.pictures or '[]')
                })
        
        return {"itineraries": itineraries}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/itineraries/search", status_code=status.HTTP_200_OK)
def search_itineraries(search: CitySearch, db: Session = Depends(get_db)):
    try:
        itineraries = db.query(ItineraryInfo).filter_by(city=search.city).all()
        results = []
        for itinerary in itineraries:
            results.append({
                'city': itinerary.city,
                'activity_id': itinerary.activity_id,
                'activity_name': itinerary.activity_name,
                'activity_details': itinerary.activity_details,
                'price_amount': itinerary.price_amount,
                'price_currency': itinerary.price_currency,
                'pictures': json.loads(itinerary.pictures or '[]'),
                'num_users_saved': itinerary.num_users_saved
            })
        
        return {"itineraries": results}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search/flights", status_code=status.HTTP_200_OK)
def search_flights(search: FlightSearch, db: Session = Depends(get_db)):
    try:
        # Find segments matching the criteria
        segments = db.query(SegmentInfo).filter_by(
            departure_airport=search.departure_airport,
            destination_airport=search.destination_airport
        ).all()
        
        flight_ids = set([segment.flight_id for segment in segments])
        results = []
        
        for flight_id in flight_ids:
            flight_info = db.query(FlightInfo).filter_by(flight_id=flight_id).first()
            if flight_info:
                all_segments = db.query(SegmentInfo).filter_by(flight_id=flight_id).all()
                segments_data = [{
                    'index': seg.index,
                    'segment_id': seg.segment_id,
                    'airline_code': seg.airline_code,
                    'flight_code': seg.flight_code,
                    'departure_date': seg.departure_date,
                    'departure_time': seg.departure_time,
                    'arrival_date': seg.arrival_date,
                    'arrival_time': seg.arrival_time,
                    'duration': seg.duration,
                    'departure_airport': seg.departure_airport,
                    'destination_airport': seg.destination_airport
                } for seg in all_segments]
                
                results.append({
                    'flight_id': flight_info.flight_id,
                    'total_num_segments': flight_info.total_num_segments,
                    'price': flight_info.price,
                    'segments': segments_data,
                    'num_users_saved': flight_info.num_users_saved
                })
        
        return {"flights": results}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)