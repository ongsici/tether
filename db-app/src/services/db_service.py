from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict, Any, Union, Generator, Callable
import os
from dotenv import load_dotenv
from functools import wraps
import json

# Import your models
from ..models.db_model import Base, User, SavedFlight, FlightInfo, SegmentInfo, SavedItinerary, ItineraryInfo

# Load environment variables
load_dotenv()

# Determine environment
ENV = os.getenv("ENVIRONMENT", "development")

# Database configuration
if ENV == "production":
    DB_HOST = os.getenv("DB_HOST", "tether-database.postgres.database.azure.com")
    DB_NAME = os.getenv("DB_NAME", "flight_itinerary")
    DB_USER = os.getenv("DB_USER", "dbadmin")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    # Create PostgreSQL connection URL
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    # Use SQLite for development
    DATABASE_URL = "sqlite:///flight_itinerary.db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(engine)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database session context manager
def get_db_session() -> Generator[Session, None, None]:
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper to handle database operations with error handling
def db_operation(func: Callable) -> Callable:
    """Decorator for database operations with error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            result = func(db=db, *args, **kwargs)
            db.commit()
            return result
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        finally:
            db.close()
    return wrapper

# User operations
@db_operation
def create_user(user_id: str, user_details: Optional[str] = None, db: Session = None) -> Dict[str, str]:
    """Create a new user"""
    db_user = User(user_id=user_id, user_details=user_details or "")
    db.add(db_user)
    return {"message": "User created successfully"}

@db_operation
def get_user(user_id: str, db: Session = None) -> Dict[str, str]:
    """Get user details"""
    db_user = db.query(User).filter_by(user_id=user_id).first()
    if not db_user:
        return None
    return {"user_id": db_user.user_id, "user_details": db_user.user_details}

# Flight operations
@db_operation
def save_flight(
    user_id: str,
    flight_id: str,
    total_num_segments: int,
    price: str,
    segments: List[Dict[str, Any]],
    db: Session = None
) -> Dict[str, str]:
    """Save a flight for a user"""
    # Check if flight exists, if not create it
    db_flight = db.query(FlightInfo).filter_by(flight_id=flight_id).first()
    if not db_flight:
        db_flight = FlightInfo(
            flight_id=flight_id,
            total_num_segments=total_num_segments,
            price=price,
            num_users_saved=1
        )
        db.add(db_flight)
        
        # Add segment information
        for segment in segments:
            seg = SegmentInfo(
                flight_id=flight_id,
                index=segment["index"],
                segment_id=segment["segment_id"],
                airline_code=segment["airline_code"],
                flight_code=segment["flight_code"],
                departure_date=segment["departure_date"],
                departure_time=segment["departure_time"],
                arrival_date=segment["arrival_date"],
                arrival_time=segment["arrival_time"],
                duration=segment["duration"],
                departure_airport=segment["departure_airport"],
                destination_airport=segment["destination_airport"]
            )
            db.add(seg)
    else:
        # Increment number of users who saved this flight
        db_flight.num_users_saved += 1
    
    # Create saved flight entry
    saved_flight = SavedFlight(user_id=user_id, flight_id=flight_id)
    db.add(saved_flight)
    
    return {"message": "Flight saved successfully"}

@db_operation
def unsave_flight(user_id: str, flight_id: str, db: Session = None) -> Dict[str, str]:
    """Remove a saved flight for a user"""
    saved_flight = db.query(SavedFlight).filter_by(
        user_id=user_id, 
        flight_id=flight_id
    ).first()
    
    if not saved_flight:
        return None
    
    flight_info = db.query(FlightInfo).filter_by(flight_id=flight_id).first()
    if flight_info and flight_info.num_users_saved > 0:
        flight_info.num_users_saved -= 1
    
    db.delete(saved_flight)
    
    return {"message": "Flight removed from saved"}

@db_operation
def get_saved_flights(user_id: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:
    """Get all saved flights for a user"""
    saved_flights = db.query(SavedFlight).filter_by(user_id=user_id).all()
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

@db_operation
def search_flights(departure_airport: str, destination_airport: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:
    """Search flights by departure and destination airports"""
    # Find segments matching the criteria
    segments = db.query(SegmentInfo).filter_by(
        departure_airport=departure_airport,
        destination_airport=destination_airport
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

# Itinerary operations
@db_operation
def save_itinerary(
    user_id: str,
    city: str,
    activity_id: str,
    activity_name: str,
    activity_details: str,
    price_amount: str,
    price_currency: str,
    pictures: Optional[List[str]] = None,
    db: Session = None
) -> Dict[str, str]:
    """Save an itinerary for a user"""
    # Check if itinerary exists, if not create it
    db_itinerary = db.query(ItineraryInfo).filter_by(activity_id=activity_id).first()
    if not db_itinerary:
        db_itinerary = ItineraryInfo(
            city=city,
            activity_id=activity_id,
            activity_name=activity_name,
            activity_details=activity_details,
            price_amount=price_amount,
            price_currency=price_currency,
            pictures=json.dumps(pictures or []),
            num_users_saved=1
        )
        db.add(db_itinerary)
    else:
        # Increment number of users who saved this itinerary
        db_itinerary.num_users_saved += 1
    
    # Create saved itinerary entry
    saved_itinerary = SavedItinerary(user_id=user_id, activity_id=activity_id)
    db.add(saved_itinerary)
    
    return {"message": "Itinerary saved successfully"}

@db_operation
def unsave_itinerary(user_id: str, activity_id: str, db: Session = None) -> Dict[str, str]:
    """Remove a saved itinerary for a user"""
    saved_itinerary = db.query(SavedItinerary).filter_by(
        user_id=user_id, 
        activity_id=activity_id
    ).first()
    
    if not saved_itinerary:
        return None
    
    itinerary_info = db.query(ItineraryInfo).filter_by(activity_id=activity_id).first()
    if itinerary_info and itinerary_info.num_users_saved > 0:
        itinerary_info.num_users_saved -= 1
    
    db.delete(saved_itinerary)
    
    return {"message": "Itinerary removed from saved"}

@db_operation
def get_saved_itineraries(user_id: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:
    """Get all saved itineraries for a user"""
    saved_itineraries = db.query(SavedItinerary).filter_by(user_id=user_id).all()
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

@db_operation
def search_itineraries(city: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:
    """Search itineraries by city"""
    itineraries = db.query(ItineraryInfo).filter_by(city=city).all()
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