from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, IntegrityError
from typing import Optional, List, Dict, Any, Callable
from functools import wraps
import logging
import time

from ..utils.api_client import get_db
from ..models.db_model import SavedFlight, FlightInfo, FlightSegments, SegmentInfo, SavedItinerary, ItineraryInfo
from ..models.payload_model import (
    SegmentResponse, SegmentResponseWrapper, FlightResponseObj,
    FlightResponseObjWrapper, FlightViewResponse, ItineraryDetails, ItineraryViewResponse,
    SaveUnsaveResponse
)
from ..models.convert_model import FlightSaveDB

logger = logging.getLogger("db_microservice")

# helper to handle database operations with logging/error handling
def db_operation(func: Callable) -> Callable:
    """Decorator for database operations with error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        operation_id = f"{func.__name__}_{time.time():.0f}" # generate unique operation ID
        logger.debug(f"Database operation starting: {func.__name__} [ID:{operation_id}]")
        start_time = time.time()
        
        db: Session = next(get_db())
        try:
            # execute the database operation
            result = func(db=db, *args, **kwargs)
            db.commit()
            
            elapsed_time = time.time() - start_time
            logger.debug(f"Database operation completed: {func.__name__} [ID:{operation_id}] - Time: {elapsed_time:.3f}s")
            return result
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error in {func.__name__} [ID:{operation_id}]: {str(e)}", exc_info=True)
            raise
            
        except NoResultFound as e:
            db.rollback()
            logger.warning(f"Resource not found in {func.__name__} [ID:{operation_id}]")
            raise
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error in {func.__name__} [ID:{operation_id}]: {str(e)}", exc_info=True)
            raise
            
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error in {func.__name__} [ID:{operation_id}]: {str(e)}", exc_info=True)
            raise
            
        finally:
            db.close()
            
    return wrapper


############### FLIGHTS ###############

@db_operation
def save_flight(full_info: FlightSaveDB, db: Session = None) -> Dict[str, str]:
    """
    Saves flight for user
    Creates new flight record if it does not exist
    Else, updates existing flight information
    """
    flight_info = full_info.flight
    segments = full_info.segments
    flight_segments = full_info.flight_segments
    
    # [1] check if flight record already exists
    db_flight = db.query(FlightInfo).filter_by(flight_id=flight_info.flight_id).one_or_none()

    if not db_flight:
        logger.info(f"Creating new flight record for flight {flight_info.flight_id}")

        # (a) save flight info
        db.add(FlightInfo(**flight_info.model_dump(), num_users_saved=1))
        db.flush()

        # (b) save segments info
        for segment_info in segments:
            logger.debug(f"Processing segment {segment_info.segment_id} for flight {flight_info.flight_id}")
            
            # check if segment already exists
            db_segment = db.query(SegmentInfo).filter_by(segment_id=segment_info.segment_id).one_or_none()

            if not db_segment:
                logger.debug(f"Creating new segment record for segment {segment_info.segment_id}")
                db.add(SegmentInfo(**segment_info.model_dump(), num_flights_saved=1))
            else:
                logger.debug(f"Updating existing segment {segment_info.segment_id}")
                db_segment.num_flights_saved += 1
            
            db.flush()

        # (c) save connecting flights info
        logger.debug(f"Saving {len(flight_segments)} flight-segment relationships")
        db.bulk_save_objects([FlightSegments(**fs.model_dump()) for fs in flight_segments])
    
    # increment users saved if flight info already exists
    else:
        logger.info(f"Updating existing flight {flight_info.flight_id}")
        db_flight.num_users_saved += 1

    # [2] add to user saved flights, if not already saved
    existing_saved_flight = db.query(SavedFlight).filter_by(
        user_id=full_info.user_id,
        flight_id=flight_info.flight_id
    ).one_or_none()

    if existing_saved_flight:
        logger.info(f"User {full_info.user_id} has already saved flight {flight_info.flight_id}")
        # return {"message": "User has already saved this flight"}
        return SaveUnsaveResponse(user_id=full_info.user_id, status=False, message="User already saved flight")
    
    db.add(SavedFlight(user_id=full_info.user_id, flight_id=flight_info.flight_id))
    db.commit()
    # return {"message": "Flight saved successfully"}
    return SaveUnsaveResponse(user_id=full_info.user_id, status=True, message="Flight saved successfully")


@db_operation
def unsave_flight(user_id: str, flight_id: str, db: Session = None) -> Optional[Dict[str, str]]:
    """
    Remove flight from user saved flights
    Cleans up flight info if no users have saved it
    """
    # [1] check if flight in user saved flights
    saved_flight = db.query(SavedFlight).filter_by(
        user_id=user_id,
        flight_id=flight_id
    ).one_or_none()
    
    if not saved_flight:
        logger.warning(f"Flight {flight_id} not found saved for user {user_id}")
        # return {"message": "User does not have this flight saved"}
        return SaveUnsaveResponse(user_id=user_id, status=False, message="User does not have this flight saved")
    
    # retrieve flight info before deleting saved flight
    flight_info = db.query(FlightInfo).filter_by(flight_id=flight_id).one_or_none()
    
    if not flight_info:
        logger.warning(f"Record for flight {flight_id} not found")
        # return {"message": "Flight does not exist"}
        return SaveUnsaveResponse(user_id=user_id, status=False, message="Flight does not exist")

    # [2] delete from user saved flights
    db.delete(saved_flight)
    db.flush()

    # decrement num_users_saved count
    flight_info.num_users_saved -= 1
    logger.debug(f"Updated flight {flight_id} users saved count to {flight_info.num_users_saved}")

    # [3] delete all related flight info if no other users saved it
    if flight_info.num_users_saved == 0:
        logger.info(f"No users have saved flight {flight_id}, cleaning up flight data")
        
        segment_ids = [row[0] for row in db.query(FlightSegments.segment_id)
                        .filter(FlightSegments.flight_id == flight_id).all()]
        
        logger.debug(f"Found {len(segment_ids)} segments associated with flight {flight_id}")

        # [a] delete flight segments (child)
        db.query(FlightSegments).filter_by(flight_id=flight_id).delete()
        db.flush()

        # [b] delete flight info (parent)
        db.delete(flight_info)
        db.flush()

        # [c] update/delete segment info
        for segment_id in segment_ids:
            logger.debug(f"Processing segment {segment_id} for cleanup")
            segment_info = db.query(SegmentInfo).filter_by(segment_id=segment_id).one_or_none()

            if segment_info:
                segment_info.num_flights_saved -= 1

                if segment_info.num_flights_saved <= 0:
                    logger.debug(f"Deleting segment {segment_id}, which is no longer in use")
                    db.delete(segment_info)
                else:
                    logger.debug(f"Updated segment {segment_id} flight count to {segment_info.num_flights_saved}")
    
    # return {"message": "Flight successfully removed from saved"}
    return SaveUnsaveResponse(user_id=user_id, status=True, message="Flight successfully removed from saved")

@db_operation
def get_saved_flights(user: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:
    # get all saved flights for user
    saved_flights = db.query(SavedFlight).filter(SavedFlight.user_id == user).all()
    logger.debug(f"Found {len(saved_flights)} saved flights for user {user}")

    all_flights = []

    for flight in saved_flights:
        logger.debug(f"Processing flight {flight.flight_id}")
        flight_info = db.query(FlightInfo).filter(FlightInfo.flight_id == flight.flight_id).one_or_none()

        if not flight_info:
            logger.warning(f"Flight info not found for {flight.flight_id}, skipping")
            continue

        # get outbound flight segments
        outbound_segment_info = (
            db.query(SegmentInfo, FlightSegments.segment_order)
            .join(FlightSegments, SegmentInfo.segment_id == FlightSegments.segment_id)
            .filter(FlightSegments.flight_id == flight.flight_id)
            .filter(FlightSegments.bound == 'outbound')
            .all()
        )
        
        # get inbound flight segments
        inbound_segment_info = (
            db.query(SegmentInfo, FlightSegments.segment_order)
            .join(FlightSegments, SegmentInfo.segment_id == FlightSegments.segment_id)
            .filter(FlightSegments.flight_id == flight.flight_id)
            .filter(FlightSegments.bound == 'inbound')
            .all()
        )

        logger.debug(f"Found {len(outbound_segment_info)} outbound and {len(inbound_segment_info)} inbound segments")

        # process outbound flights
        outbound_flights = []
        for out_f, segment_order in outbound_segment_info:
            outbound_flights.append(SegmentResponseWrapper(
                SegmentResponse=SegmentResponse(
                    num_passengers = 1,                     # TODO: check if save num_passengers
                    departure_time = out_f.departure_time,
                    departure_date = out_f.departure_date,
                    arrival_date = out_f.arrival_date,
                    arrival_time = out_f.arrival_time,
                    duration = out_f.duration,
                    departure_airport = out_f.departure_airport,
                    departure_city = out_f.departure_city,
                    destination_airport = out_f.destination_airport,
                    destination_city = out_f.destination_city,
                    airline_code = out_f.airline_code,
                    flight_number = str(segment_order),
                    unique_id = out_f.segment_id
                )
            ))
        
        # process inbound flights
        inbound_flights = []
        for in_f, segment_order in inbound_segment_info:
            inbound_flights.append(SegmentResponseWrapper(
                SegmentResponse=SegmentResponse(
                    num_passengers = 1,                     # TODO: check if save num_passengers
                    departure_time = in_f.departure_time,
                    departure_date = in_f.departure_date,
                    arrival_date = in_f.arrival_date,
                    arrival_time = in_f.arrival_time,
                    duration = in_f.duration,
                    departure_airport = in_f.departure_airport,
                    departure_city=in_f.destination_city,
                    destination_airport = in_f.destination_airport,
                    destination_city=in_f.destination_city,
                    airline_code = in_f.airline_code,
                    flight_number = str(segment_order),
                    unique_id = in_f.segment_id
                )
            ))

        all_flights.append(FlightResponseObjWrapper(
            FlightResponse=FlightResponseObj(
                number_of_segments = flight_info.total_num_segments,
                flight_id = flight.flight_id,
                outbound = outbound_flights,
                inbound = inbound_flights,
                price_per_person = flight_info.price_per_person,
                total_price = flight_info.total_price
            )
        ))
            
    logger.info(f"Successfully retrieved {len(all_flights)} flights for user {user}")
    response = FlightViewResponse(user_id=user, flights=all_flights)

    return response


############### ITINERARY ###############
@db_operation
def save_itinerary(user_id: str, city: str, activity_id: str, activity_name: str, activity_details: str, price_amount: str, price_currency: str, pictures: str, db: Session = None) -> Dict[str, str]:
    """
    Saves itinerary for user
    Creates new itinerary record if it does not exist
    """
    # [1] check if itinerary exists
    db_itinerary = db.query(ItineraryInfo).filter_by(activity_id=activity_id).one_or_none()

    if not db_itinerary:
        logger.info(f"Creating new itinerary record for {activity_id}")
        db_itinerary = ItineraryInfo(
            city=city, activity_id=activity_id, activity_name=activity_name,
            activity_details=activity_details, price_amount=price_amount,
            price_currency=price_currency, pictures=pictures, num_users_saved=1)
        db.add(db_itinerary)
    else:
        logger.info(f"Updating existing itinerary {activity_id}")
        db_itinerary.num_users_saved += 1
    
    # [2] check that user has not already saved this itinerary
    existing_saved_itinerary = db.query(SavedItinerary).filter_by(user_id=user_id, activity_id=activity_id).one_or_none()
    if existing_saved_itinerary:
        logger.info(f"User {user_id} has already saved itinerary {activity_id}")
        # return {"message": "User has already saved this itinerary"}
        return SaveUnsaveResponse(user_id=user_id, status=False, message="User already saved itinerary")
    
    db.add(SavedItinerary(user_id=user_id, activity_id=activity_id))
    # return {"message": "Itinerary saved successfully"}
    return SaveUnsaveResponse(user_id=user_id, status=True, message="Itinerary saved successfully")

@db_operation
def unsave_itinerary(user_id: str, activity_id: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Remove itinerary from user saved itineraries
    Cleans up itinerary info if no users have saved it
    """
    # [1] check if itinerary in user saved itineraries
    saved_itinerary = db.query(SavedItinerary).filter_by(
        user_id=user_id,
        activity_id=activity_id
    ).one_or_none()

    if not saved_itinerary:
        logger.warning(f"Itinerary {activity_id} not found saved for user {user_id}")
        # return {"message": "User does not have this itinerary saved"}
        return SaveUnsaveResponse(user_id=user_id, status=False, message="User does not have this itinerary saved")
 
    # [2] delete from user saved itineraries
    db.delete(saved_itinerary)
    db.flush()
    
    # [3] update or delete itinerary info
    itinerary_info = db.query(ItineraryInfo).filter_by(activity_id=activity_id).one_or_none()

    if itinerary_info:
        # [a] decrement num_users_saved in the ItineraryInfo table
        itinerary_info.num_users_saved = max(0, itinerary_info.num_users_saved - 1)
        logger.debug(f"Updated itinerary {activity_id} users saved count to {itinerary_info.num_users_saved}")

        # [b] delete entry if no users saved this itinerary
        if itinerary_info.num_users_saved == 0:
            logger.info(f"No users have saved itinerary {activity_id}, deleting record")
            db.delete(itinerary_info)
    else:
        logger.warning(f"Itinerary information for {activity_id} not found")
    
    # return {"message": "Itinerary removed from saved"}
    return SaveUnsaveResponse(user_id=user_id, status=True, message="Itinerary removed from saved")

@db_operation
def get_saved_itineraries(user_id: str, db: Session = None) -> Dict[str, List[Dict[str, Any]]]:    
    activities = (
        db.query(ItineraryInfo)
        .join(SavedItinerary, ItineraryInfo.activity_id == SavedItinerary.activity_id)
        .filter(SavedItinerary.user_id == user_id)
        .all()
    )

    logger.debug(f"Found {len(activities)} saved itineraries for user {user_id}")

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

    logger.info(f"Successfully retrieved {len(itinerary_list)} saved itineraries for user {user_id}")
    response = ItineraryViewResponse(user_id=user_id, itinerary=itinerary_list)
    return response