from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict, Any, Callable
from functools import wraps
from ..utils.api_client import get_db
from ..models.db_model import SavedFlight, FlightInfo, FlightSegments, SegmentInfo, SavedItinerary, ItineraryInfo
from ..models.payload_model import SegmentResponse, SegmentResponseWrapper, FlightResponseObj, FlightResponseObjWrapper, FlightViewResponse, ItineraryDetails, ItineraryViewResponse
from ..models.convert_model import FlightSaveDB


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
def save_flight(full_info: FlightSaveDB, db: Session = None) -> Dict[str, str]:
    flight_info = full_info.flight
    segments = full_info.segments
    flight_segments = full_info.flight_segments
    
    # check if flight already exists in FlightInfo
    db_flight = db.query(FlightInfo).filter_by(flight_id=flight_info.flight_id).one_or_none()
    if not db_flight:
        # (1) save flight info
        db.add(FlightInfo(**flight_info.dict(), num_users_saved=1))  # Pydantic v2
        db.commit()

        # (2) save segments info
        for segment_info in segments:
            # check if segment already exists
            db_segment = db.query(SegmentInfo).filter_by(segment_id=segment_info.segment_id).one_or_none()
            if not db_segment:
                db.add(SegmentInfo(**segment_info.dict(), num_flights_saved=1))
                db.commit()
            else:
                db_segment.num_flights_saved += 1

        # (3) save connecting flights info
        db.bulk_save_objects([FlightSegments(**fs.dict()) for fs in flight_segments])
        db.commit()
    
    # flight info already exists, so only need to increment users saved
    else:
        db_flight.num_users_saved += 1
        db.commit()

    # add to user's saved flights list
    # check that user has not already saved this flight
    existing_saved_flight = db.query(SavedFlight).filter_by(user_id=full_info.user_id, flight_id=flight_info.flight_id).one_or_none()
    if existing_saved_flight:
        return {"message": "User has already saved this flight"}
    
    db.add(SavedFlight(user_id=full_info.user_id, flight_id=flight_info.flight_id))
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
        flight_info.num_users_saved -= 1
        db.commit()
        
        # delete all related flight info if no other users saved it
        if flight_info.num_users_saved == 0:

            # (1) check if other flights saved corresponding segments
            segment_ids = db.query(FlightSegments.segment_id).filter(FlightSegments.flight_id == flight_id).all()
            for s in segment_ids:
                segment_info = db.query(SegmentInfo).filter_by(segment_id=s).one_or_none()
                if segment_info:
                    segment_info.num_flights_saved -= 1
                    db.commit()

                    # (2) delete segments if no other flights use it
                    if segment_info.num_flights_saved == 0:
                        db.delete(segment_info)
                        db.commit()

                # TODO: improve error handling
                else:
                    return {"message": "Flight segment does not exist"}

            # (3) delete connecting flight info
            db.query(FlightSegments).filter_by(flight_id=flight_id).delete()
            db.commit()
            
            # (4) delete flight info
            db.delete(flight_info)
            db.commit()

    # TODO: improve error handling
    else:
        return {"message": "Flight does not exist"}
    
    return {"message": "Flight successfully removed from saved"}


@db_operation
def get_saved_flights(user: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:
    all_flights = []

    for flight in db.query(SavedFlight).filter(SavedFlight.user_id == user).all():
        flight_info = db.query(FlightInfo).filter(FlightInfo.flight_id == flight.flight_id).one_or_none()

        outbound_flights = []
        inbound_flights = []

        outbound_segment_info = (
            db.query(SegmentInfo)
            .join(FlightSegments, SegmentInfo.segment_id == FlightSegments.segment_id)
            .filter(FlightSegments.flight_id == flight.flight_id)
            .filter(FlightSegments.bound == 'outbound')
            .all()
        )
        inbound_segment_info = (
            db.query(SegmentInfo)
            .join(FlightSegments, SegmentInfo.segment_id == FlightSegments.segment_id)
            .filter(FlightSegments.flight_id == flight.flight_id)
            .filter(FlightSegments.bound == 'inbound')
            .all()
        )

        for out_f in outbound_segment_info:
            outbound_flights.append(SegmentResponseWrapper(SegmentResponse(
                num_passengers = 1,                     # TODO: check if save num_passengers
                departure_time = out_f.departure_time,
                departure_date = out_f.departure_date,
                arrival_date = out_f.arrival_date,
                arrival_time = out_f.arrival_time,
                duration = out_f.duration,
                departure_airport = out_f.departure_airport,
                destination_airport = out_f.destination_airport,
                airline_code = out_f.airline_code,
                flight_number = out_f.flight_number,
                unique_id = out_f.segment_id
            )))
        for in_f in inbound_segment_info:
            inbound_flights.append(SegmentResponseWrapper(SegmentResponse(
                num_passengers = 1,                     # TODO: check if save num_passengers
                departure_time = in_f.departure_time,
                departure_date = in_f.departure_date,
                arrival_date = in_f.arrival_date,
                arrival_time = in_f.arrival_time,
                duration = in_f.duration,
                departure_airport = in_f.departure_airport,
                destination_airport = in_f.destination_airport,
                airline_code = in_f.airline_code,
                flight_number = in_f.flight_number,
                unique_id = in_f.segment_id
            )))

        all_flights.append(FlightResponseObjWrapper(
            FlightResponse=FlightResponseObj(
                number_of_segments = flight_info.total_num_segments,
                flight_id = flight.flight_id,
                outbound = outbound_flights,
                inbound = inbound_flights,
                price_per_person = flight_info.price
            )
        ))
            
    
    response = FlightViewResponse(user_id=user, flights=all_flights)

    return response


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
def unsave_itinerary(user_id: str, activity_id: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:
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
    activities = (
        db.query(ItineraryInfo)
        .join(SavedItinerary, ItineraryInfo.activity_id == SavedItinerary.activity_id)
        .filter(SavedItinerary.user_id == user_id)
        .all()
    )

    itinerary_list = []
    for a in activities:
        itinerary_list.append(ItineraryDetails(
            city = a.city,
            activity_id = a.activity_id,
            activity_name = a.activity_name,
            activity_details = a.activity_details,
            price_amount = a.price_amount,
            price_currency = a.price_currency,
            pictures = a.pictures
        ))

    response = ItineraryViewResponse(user_id=user_id, itinerary=itinerary_list)
    return response