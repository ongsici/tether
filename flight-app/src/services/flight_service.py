from ..utils.api_client import get_flight_data
from ..models.flight_model import FlightResponse, SegmentResponse, FlightResponseObj, FlightResponseObjWrapper, SegmentResponseWrapper
from ..utils.custom_logging import configure_logging
import logging
import uuid

configure_logging()
logger = logging.getLogger("flight_microservice")

def get_flights(origin_loc_code: str, destination_loc_code: str, num_passenger: str, 
                    departure_date: str, return_date: str, user_id: str) -> FlightResponse:
    logger.info(f"Calling get_flight_data for departure_date: {departure_date}, return_date: {return_date}")
    data = get_flight_data(origin_loc_code, destination_loc_code, num_passenger, departure_date, return_date)

    flights = []
    for flight in data["data"]:
        price_per_person = str(flight["price"]["base"])
        outbound_segments = []
        inbound_segments = []
        for i, itinerary in enumerate(flight["itineraries"]):
            for segment in itinerary["segments"]:
                if len(itinerary['segments']) > 3:
                    continue
                dep_date, dep_time = segment["departure"]["at"].split('T')
                arr_date, arr_time = segment["arrival"]["at"].split('T')
                airline_code = segment["carrierCode"]
                flight_code = segment["number"]

                segment_info = {
                    "num_passengers": int(num_passenger),
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
            "price_per_person": price_per_person
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
    

# def extract_flight_info(flights: FlightResponse):
#     segments = flights.segment_info
#     for i, segment in enumerate(segments):
#         next_seg_id = segments[i+1].unique_id if (i+1 < len(segments)) else None
#         # Store each field in database



