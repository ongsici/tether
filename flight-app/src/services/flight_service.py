from ..utils.api_client import get_flight_data
from ..models.flight_model import (
    FlightResponse, SegmentResponse, FlightResponseObj,
    FlightResponseObjWrapper, SegmentResponseWrapper
)
import logging
import uuid

logger = logging.getLogger("flight_microservice")

def get_flights(
    origin_loc_code: str,
    destination_loc_code: str,
    num_passenger: str,
    departure_date: str,
    return_date: str,
    user_id: str
) -> FlightResponse:
    """
    Retrieve flight data from external API and build a structured flight response.

    :param origin_loc_code: Origin Airport IATA Code
    :param destination_loc_code: Destination Airport IATA Code
    :param num_passenger: Number of passengers
    :param departure_date: Departure date
    :param return_date: Return date
    :param user_id: ID of the user requesting the flight
    :return: A FlightResponse object containing structured flight information
    """

    logger.info(
        f"Requesting flight data for: origin={origin_loc_code}, destination={destination_loc_code}, "
        f"departure_date={departure_date}, return_date={return_date}, passengers={num_passenger}"
    )

    try:
        data = get_flight_data(origin_loc_code, destination_loc_code, num_passenger, departure_date, return_date)
    except Exception as e:
        # Log at ERROR level if the external API call fails or raises an exception
        logger.error(
            "Failed to retrieve flight data from the external API. "
            f"Error: {e}",
            exc_info=True
        )
        # Depending on your error-handling strategy, re-raise or return some fallback
        raise

    # Debug the raw response for troubleshooting
    logger.debug(f"Raw flight data response: {data}")

    # Guard against missing "data" key to avoid KeyError
    if "data" not in data:
        logger.error("Flight data response is missing the 'data' key. Cannot continue.")
        raise ValueError("Flight data response does not contain 'data'.")

    flights = []
    logger.info(f"Number of flights returned by the API: {len(data['data'])}")

    for idx, flight in enumerate(data["data"]):
        # Debug-level log for each flight to aid in step-by-step tracing
        logger.debug(f"Processing flight index {idx}: {flight}")

        # Check if flight has an itinerary with more than 3 segments
        if any(len(itin["segments"]) > 3 for itin in flight.get("itineraries", [])):
            logger.warning(
                f"Skipping flight index {idx} because it has an itinerary with more than 3 segments."
            )
            continue

        # Retrieve base price; wrap in try-except in case `price` key is missing
        try:
            price_per_person = str(flight["price"]["base"])
        except KeyError:
            logger.error(
                f"Skipping flight index {idx}: Missing 'price' or 'base' key in flight data. Flight: {flight}"
            )
            continue

        outbound_segments = []
        inbound_segments = []

        # Iterate itineraries
        for i, itinerary in enumerate(flight.get("itineraries", [])):
            logger.debug(
                f"  Processing itinerary {i} for flight index {idx}, containing "
                f"{len(itinerary.get('segments', []))} segment(s)."
            )
            # Build segment info
            for segment in itinerary.get("segments", []):
                try:
                    dep_date, dep_time = segment["departure"]["at"].split('T')
                    arr_date, arr_time = segment["arrival"]["at"].split('T')
                    airline_code = segment["carrierCode"]
                    flight_code = segment["number"]
                except (KeyError, ValueError) as e:
                    logger.error(
                        f"    Skipping segment due to missing or invalid data: {segment}. Error: {e}",
                        exc_info=True
                    )
                    continue

                segment_info = {
                    "num_passengers": int(num_passenger),
                    "departure_time": dep_time,
                    "departure_date": dep_date,
                    "arrival_date": arr_date,
                    "arrival_time": arr_time,
                    "duration": segment["duration"][2:],  # Remove "PT" prefix from duration
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

        # Build the flight object
        number_of_segments = len(outbound_segments) + len(inbound_segments)
        flight_info = {
            "number_of_segments": number_of_segments,
            "flight_id": str(uuid.uuid4()),
            "outbound": outbound_segments,
            "inbound": inbound_segments,
            "price_per_person": price_per_person
        }

        flight_obj = FlightResponseObj(**flight_info)
        flights.append(FlightResponseObjWrapper(FlightResponse=flight_obj))

    # Build the final FlightResponse
    flights_response = FlightResponse(
        user_id=user_id,
        results=flights
    )

    logger.info(
        f"Constructed FlightResponse with {len(flights)} flight(s) for user_id={user_id}. "
        f"Departure date: {departure_date}, Return date: {return_date}"
    )

    logger.debug(f"Final FlightResponse object: {flights_response}")

    return flights_response
    

# def extract_flight_info(flights: FlightResponse):
#     segments = flights.segment_info
#     for i, segment in enumerate(segments):
#         next_seg_id = segments[i+1].unique_id if (i+1 < len(segments)) else None
#         # Store each field in database



