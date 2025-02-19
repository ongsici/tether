from ..utils.api_client import get_flight_data
from ..models.flight_model import FlightResponse, SegmentResponse
from ..utils.logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger("flight_microservice")

def get_flights(origin_loc_code: str, destination_loc_code: str, num_passenger: str, 
                    departure_date: str, return_date: str = None) -> FlightResponse:
    logger.info(f"Calling get_flight_data for departure_date: {departure_date}, return_date: {return_date}")
    data = get_flight_data(origin_loc_code, destination_loc_code, num_passenger, departure_date, return_date)

    flights = []
    for flight in data["data"]:
        price_per_person = flight["price"]["base"]
        segments = []
        for itinerary in flight["itineraries"]:
            for segment in itinerary["segments"]:
                if len(itinerary['segments']) > 3:
                    continue
                dep_date, dep_time = segment["departure"]["at"].split('T')
                arr_date, arr_time = segment["arrival"]["at"].split('T')
                airline_code = segment['carrierCode']
                flight_code = segment['number']

                segment_info = {
                    "num_passengers": num_passenger,
                    "departure_time": dep_time,
                    "departure_date": dep_date,
                    "arrival_date": arr_date,
                    "arrival_time": arr_time,
                    "duration": segment["duration"][2:],
                    "departure_airport": segment["departure"]["iataCode"],
                    "destination_airport": segment["arrival"]["iataCode"],
                    "airline_code": airline_code,
                    "flight_number": flight_code,
                    "unique_id": airline_code + flight_code + departure_date + dep_time
                }
                segments.append(SegmentResponse(**segment_info))
        flight_info = {
            "number_of_segments": len(segments),
            "segment_info": segments,
            "price_per_person": price_per_person
        }
        flights.append(FlightResponse(**flight_info))
    
    logger.info(f"get_flight_data successful for departure_date: {departure_date}, return_date: {return_date}")
    return flights

def extract_flight_info(flights: FlightResponse):
    segments = flights.segment_info
    for i, segment in enumerate(segments):
        next_seg_id = segments[i+1].unique_id if (i+1 < len(segments)) else None
        # Store each field in database



