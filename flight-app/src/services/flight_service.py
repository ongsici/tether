from ..utils.api_client import get_flight_data
from ..models.flight_model import FlightResponse, SegmentResponse, FlightResponseObj, FlightResponseObjWrapper, SegmentResponseWrapper
from ..utils.custom_logging import configure_logging
import logging
import uuid
import json
import os

configure_logging()
logger = logging.getLogger("flight_microservice")

def get_flights(origin_loc_code: str, destination_loc_code: str, num_passenger: str, 
                    departure_date: str, return_date: str, user_id: str) -> FlightResponse:
    logger.info(f"Calling get_flight_data for departure_date: {departure_date}, return_date: {return_date}")
    data = get_flight_data(origin_loc_code, destination_loc_code, num_passenger, departure_date, return_date)

    flights = []
    for flight in data["data"]:
        if any(len(itin["segments"]) > 3 for itin in flight["itineraries"]):
            logger.info("Skipping a flight because it has an itinerary with more than 3 segments.")
            continue
        price_per_person = str(flight["price"]["base"])
        outbound_segments = []
        inbound_segments = []
        for i, itinerary in enumerate(flight["itineraries"]):
            for segment in itinerary["segments"]:
                dep_date, dep_time = segment["departure"]["at"].split('T')
                dep_time = dep_time[:5]
                arr_date, arr_time = segment["arrival"]["at"].split('T')
                arr_time = arr_time[:5]
                airline_code = segment["carrierCode"]
                flight_code = segment["number"]
                dep_airport = segment["departure"]["iataCode"]
                arr_airport = segment["arrival"]["iataCode"]
                dep_city = get_city_from_airport(dep_airport)
                arr_city = get_city_from_airport(arr_airport)

                segment_info = {
                    "num_passengers": int(num_passenger),
                    "departure_time": dep_time,
                    "departure_date": dep_date,
                    "arrival_date": arr_date,
                    "arrival_time": arr_time,
                    "duration": segment["duration"][2:], 
                    "departure_airport": dep_airport,
                    "departure_city": dep_city,
                    "destination_airport": arr_airport,
                    "destination_city": arr_city,
                    "airline_code": airline_code,
                    "flight_number": flight_code,
                    "unique_id": airline_code + flight_code + departure_date + dep_time
                }

                wrapped_segment = SegmentResponseWrapper(
                    SegmentResponse=SegmentResponse(**segment_info)
                )

                if i == 0:
                    outbound_segments.append(wrapped_segment)
                else:
                    inbound_segments.append(wrapped_segment)

        number_of_segments = len(outbound_segments) + len(inbound_segments)

        flight_info = {
            "number_of_segments": number_of_segments,
            "flight_id": str(uuid.uuid4()),
            "outbound": outbound_segments,
            "inbound": inbound_segments,
            "price_per_person": price_per_person,
            "total_price": str(round(float(price_per_person) * int(num_passenger), 2))
        }
        flight_obj = FlightResponseObj(**flight_info)

        flights.append(
            FlightResponseObjWrapper(FlightResponse=flight_obj)
        )
    
    flights_respponse = FlightResponse(
        user_id = user_id,
        results = flights
    )
    logger.info(f"get_flight_data successful for departure_date: {departure_date}, return_date: {return_date}")
    return flights_respponse
    

def get_city_from_airport(airport: str):
    file_path = os.path.join(os.getcwd(), 'src/services/airport_to_city.json')
    with open(file_path) as file:
        data = json.load(file)
    
    for entry in data:
        # Check if the airport code is in the list of airports for this entry
        if airport in entry["airports"]:
            return entry["city"]
    
    return "Unknown"

# def extract_flight_info(flights: FlightResponse):
#     segments = flights.segment_info
#     for i, segment in enumerate(segments):
#         next_seg_id = segments[i+1].unique_id if (i+1 < len(segments)) else None
#         # Store each field in database



