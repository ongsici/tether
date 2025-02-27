from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict, Any, Callable
from functools import wraps
from ..utils.api_client import get_db
from ..models.db_model import SavedFlight, FlightInfo, SegmentInfo, SavedItinerary, ItineraryInfo

# Helper to handle database operations with error handling
def db_operation(func: Callable) -> Callable:
    """Decorator for database operations with error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        db: Session = next(get_db())
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


############### FLIGHTS ###############
@db_operation
def save_flight(user_id: str, flight_id: str, total_num_segments: int, price: str, segments: List[Dict[str, Any]], db: Session = None) -> Dict[str, str]:
    db_flight = db.query(FlightInfo).filter_by(flight_id=flight_id).one_or_none()
    
    if not db_flight:
        db_flight = FlightInfo(flight_id=flight_id, total_num_segments=total_num_segments, price=price, num_users_saved=1)
        db.add(db_flight)
        db.commit()

        db.bulk_save_objects([SegmentInfo(flight_id=flight_id, **segment) for segment in segments])
        db.commit()
    
    else:
        db_flight.num_users_saved += 1
        db.commit()

    # check that user has not already saved this flight
    existing_saved_flight = db.query(SavedFlight).filter_by(user_id=user_id, flight_id=flight_id).one_or_none()
    if existing_saved_flight:
        return {"message": "User has already saved this flight"}
    
    db.add(SavedFlight(user_id=user_id, flight_id=flight_id))
    db.commit()
    return {"message": "Flight saved successfully"}

@db_operation
def unsave_flight(user_id: str, flight_id: str, db: Session = None) -> Optional[Dict[str, str]]:
    saved_flight = db.query(SavedFlight).filter_by(user_id=user_id, flight_id=flight_id).one_or_none()
    if not saved_flight:
        return {"message": "User does not have this flight saved"}
    
    # delete from saved_flight table
    db.delete(saved_flight)
    db.commit()
    
    flight_info = db.query(FlightInfo).filter_by(flight_id=flight_id).one_or_none()
    if flight_info:
        # decrement num_users_saved in the FlightInfo table
        flight_info.num_users_saved = max(0, flight_info.num_users_saved - 1)
        
        # delete entry if no users saved this flight
        if flight_info.num_users_saved == 0:
            # first delete corresponding segments in segment_info
            db.query(SegmentInfo).filter_by(flight_id=flight_id).delete()
            db.commit()
            
            db.delete(flight_info)
    
    db.commit()
    return {"message": "Flight removed from saved"}

@db_operation
def get_saved_flights(user_id: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:
    flights = db.query(FlightInfo).join(SavedFlight, FlightInfo.flight_id == SavedFlight.flight_id).filter(SavedFlight.user_id == user_id).all()
    return {"flights": [{
        'flight_id': f.flight_id,
        'total_num_segments': f.total_num_segments,
        'price': f.price,
        'segments': [{
            'index': s.index,
            'segment_id': s.segment_id,
            'airline_code': s.airline_code,
            'flight_code': s.flight_code,
            'departure_date': s.departure_date,
            'departure_time': s.departure_time,
            'arrival_date': s.arrival_date,
            'arrival_time': s.arrival_time,
            'duration': s.duration,
            'departure_airport': s.departure_airport,
            'destination_airport': s.destination_airport
        } for s in db.query(SegmentInfo).filter_by(flight_id=f.flight_id).all()]
    } for f in flights]}



############### ITINERARY ###############
@db_operation
def save_itinerary(user_id: str, city: str, activity_id: str, activity_name: str, activity_details: str, price_amount: str, price_currency: str, pictures: str, db: Session = None) -> Dict[str, str]:
    db_itinerary = db.query(ItineraryInfo).filter_by(activity_id=activity_id).one_or_none()

    if not db_itinerary:
        db_itinerary = ItineraryInfo(
            city=city, activity_id=activity_id, activity_name=activity_name,
            activity_details=activity_details, price_amount=price_amount,
            price_currency=price_currency, pictures=pictures, num_users_saved=1)
        db.add(db_itinerary)
    else:
        db_itinerary.num_users_saved += 1
    
    # check that user has not already saved this itinerary
    existing_saved_itinerary = db.query(SavedItinerary).filter_by(user_id=user_id, activity_id=activity_id).one_or_none()
    if existing_saved_itinerary:
        return {"message": "User has already saved this itinerary"}
    
    db.add(SavedItinerary(user_id=user_id, activity_id=activity_id))
    return {"message": "Itinerary saved successfully"}

@db_operation
def unsave_itinerary(user_id: str, activity_id: str, db: Session = None) -> Optional[Dict[str, str]]:
    saved_itinerary = db.query(SavedItinerary).filter_by(user_id=user_id, activity_id=activity_id).one_or_none()
    if not saved_itinerary:
        return {"message": "User does not have this itinerary saved"}
    
    # delete from SavedItinerary table
    db.delete(saved_itinerary)
    db.commit()
    
    itinerary_info = db.query(ItineraryInfo).filter_by(activity_id=activity_id).one_or_none()
    if itinerary_info:
        # decrement num_users_saved in the ItineraryInfo table
        itinerary_info.num_users_saved = max(0, itinerary_info.num_users_saved - 1)

        # delete entry if no users saved this itinerary
        if itinerary_info.num_users_saved == 0:
            db.delete(itinerary_info)
    
    db.commit()
    return {"message": "Itinerary removed from saved"}

@db_operation
def get_saved_itineraries(user_id: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:
    activities = db.query(ItineraryInfo).join(SavedItinerary, ItineraryInfo.activity_id == SavedItinerary.activity_id).filter(SavedItinerary.user_id == user_id).all()
    return {"activities": [{
        'city': a.city,
        'activity_id': a.activity_id,
        'activity_name': a.activity_name,
        'activity_details': a.activity_details,
        'price_amount': a.price_amount,
        'price_currency': a.price_currency,
        'pictures': a.pictures
    } for a in activities]}