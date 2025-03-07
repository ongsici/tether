from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
import logging
import time
from functools import wraps

from .services import db_service
from .models.payload_model import (
    UserRequest,
    FlightSaveRequest,
    FlightUnsaveRequest,
    ItinerarySaveRequest,
    ItineraryUnsaveRequest
)
from .models.convert_model import transform_flight_save
from .utils.logging import configure_logging

configure_logging()
logger = logging.getLogger("db_microservice")

app = FastAPI(title="Flight and Itinerary API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tether-apim-2.azure-api.net", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# middleware to enhance logging, with performance tracking
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    request_id = f"{time.time():.0f}" # generate unique request ID
    
    logger.info(f"Request started: {request.method} {request.url.path} [ID:{request_id}]")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request completed: {request.method} {request.url.path} [ID:{request_id}] - Status: {response.status_code} - Time: {process_time:.3f}s")
        return response
    except Exception as e:
        logger.error(f"Request failed: {request.method} {request.url.path} [ID:{request_id}]", exc_info=True)
        raise

# exception handling decorator (to standardise)
def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoResultFound:
            logger.warning(f"Resource not found in {func.__name__}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The requested resource was not found"
            )
        except IntegrityError as e:
            logger.error(f"Database integrity error in {func.__name__}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Data integrity error, possible duplicate entry"
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error in {func.__name__}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except ValueError as e:
            logger.warning(f"Invalid input in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )
    return wrapper

# flight endpoints
@app.post("/api/flights/save", status_code=status.HTTP_201_CREATED)
@handle_exceptions
def save_flight(flight: FlightSaveRequest):
    logger.info(f"Saving flight {flight.flights.FlightResponse.flight_id} for user {flight.user_id}")
    flight_db_info = transform_flight_save(flight)
    result = db_service.save_flight(flight_db_info)
    logger.info(f"Flight saved successfully for user {flight.user_id}")
    return result

@app.post("/api/flights/unsave", status_code=status.HTTP_200_OK)
@handle_exceptions
def unsave_flight(flight: FlightUnsaveRequest):
    logger.info(f"Removing saved flight {flight.flight_id} for user {flight.user_id}")
    result = db_service.unsave_flight(user_id=flight.user_id, flight_id=flight.flight_id)
    if not result:
        logger.warning(f"Saved flight {flight.flight_id} not found for user {flight.user_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved flight not found")
    logger.info(f"Flight removed successfully for user {flight.user_id}")
    return result

@app.get("/api/flights/get_saved", status_code=status.HTTP_200_OK)
@handle_exceptions
def get_saved_flights(user_id: str):
    logger.info(f"Retrieving saved flights for user {user_id}")
    result = db_service.get_saved_flights(user=user_id)
    # logger.info(f"Retrieved {len(result) if result else 0} saved flights for user {user.user_id}")
    return result

# itinerary endpoints
@app.post("/api/itineraries/save", status_code=status.HTTP_201_CREATED)
@handle_exceptions
def save_itinerary(itinerary: ItinerarySaveRequest):
    logger.info(f"Saving itinerary for user {itinerary.user_id} in {itinerary.itinerary.city}")
    itinerary_details = itinerary.itinerary
    result = db_service.save_itinerary(
        user_id=itinerary.user_id,
        city=itinerary_details.city,
        activity_id=itinerary_details.activity_id,
        activity_name=itinerary_details.activity_name,
        activity_details=itinerary_details.activity_details,
        price_amount=itinerary_details.price_amount,
        price_currency=itinerary_details.price_currency,
        pictures=itinerary_details.pictures
    )
    logger.info(f"Itinerary saved successfully for user {itinerary.user_id}")
    return result

@app.post("/api/itineraries/unsave", status_code=status.HTTP_200_OK)
@handle_exceptions
def unsave_itinerary(itinerary: ItineraryUnsaveRequest):
    logger.info(f"Removing saved itinerary {itinerary.activity_id} for user {itinerary.user_id}")
    result = db_service.unsave_itinerary(user_id=itinerary.user_id, activity_id=itinerary.activity_id)
    if not result:
        logger.warning(f"Saved itinerary {itinerary.activity_id} not found for user {itinerary.user_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved itinerary not found")
    logger.info(f"Itinerary removed successfully for user {itinerary.user_id}")
    return result

@app.get("/api/itineraries/get_saved", status_code=status.HTTP_200_OK)
@handle_exceptions
def get_saved_itineraries(user_id: str):
    logger.info(f"Retrieving saved itineraries for user {user_id}")
    result = db_service.get_saved_itineraries(user_id=user_id)
    # logger.info(f"Retrieved {len(result) if result else 0} saved itineraries for user {user.user_id}")
    return result

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