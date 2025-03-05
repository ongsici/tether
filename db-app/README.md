<!-- Dockerisation -->
docker buildx build --platform linux/amd64 -t ghcr.io/atchyuni/db-app:latest .
docker push ghcr.io/atchyuni/db-app:latest

# Run app locally
uvicorn src.app:app --reload

# Example itinerary request
SAVE:
curl -X 'POST' \
  'http://127.0.0.1:8000/api/itineraries/save' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "12345",
    "itinerary": {
      "city": "London",
      "activity_id": "abc123",
      "activity_name": "Piccadilly Circus",
      "activity_details": "Piccadilly Circus: the heart of London with vibrant entertainment, shopping, and dining options. A must-visit destination for fun-loving tourists.",
      "price_amount": "0.0",
      "price_currency": "EUR",
      "pictures": "https://cdn.smartvel.com/ccpictures/buildings-gdda326066_640.jpg"
    }
  }'

VIEW:
curl -X GET "http://127.0.0.1:8000/api/itineraries/get_saved?user_id=user12345"
<!-- curl -X 'POST' \
  'http://127.0.0.1:8000/api/itineraries/get_saved' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "12345" 
  }' -->

UNSAVE:
curl -X 'POST' \
  'http://127.0.0.1:8000/api/itineraries/unsave' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "12345",
    "activity_id": "abc123"
  }'


# Example flight request
SAVE:
curl -X POST "http://127.0.0.1:8000/api/flights/save" \
     -H "Content-Type: application/json" \
     -d '{
         "user_id": "123",
         "flights": {
             "FlightResponse": {
                 "number_of_segments": 1,
                 "flight_id": "XYZ123",
                 "outbound": [
                     {
                         "SegmentResponse": {
                             "num_passengers": 1,
                             "departure_time": "10:00",
                             "departure_date": "2025-03-01",
                             "arrival_date": "2025-03-01",
                             "arrival_time": "14:00",
                             "duration": "4h",
                             "departure_airport": "JFK",
                             "departure_city": "New York City",
                             "destination_airport": "LAX",
                             "destination_city": "Los Angelos",
                             "airline_code": "AA",
                             "flight_number": "1234",
                             "unique_id": "abc123"
                         }
                     }
                 ],
                 "inbound": [],
                 "price_per_person": "500",
                 "total_price": "500"
             }
         }
     }'

VIEW:
curl -X GET "http://127.0.0.1:8000/api/flights/get_saved?user_id=user123"
<!-- curl -X 'POST' \
  'http://127.0.0.1:8000/api/flights/get_saved' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "123" 
  }' -->

UNSAVE:
curl -X 'POST' \
  'http://127.0.0.1:8000/api/flights/unsave' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "123",
    "flight_id": "XYZ123"
  }'


## Using PostgreSQL database:
To run: psql -h tether-database.postgres.database.azure.com -p 5432 -U tether_postgres_admin postgres
To exit: \q