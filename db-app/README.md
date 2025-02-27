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
curl -X 'POST' \
  'http://127.0.0.1:8000/api/itineraries/get_saved' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "12345" 
  }'

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
        "user_id": "user123",
        "flight": {
            "flight_id": "abc123",
            "total_num_segments": 2,
            "price": "716.00",
            "segments": [
                {
                    "index": 1,
                    "segment_id": 1,
                    "airline_code": "TR",
                    "flight_code": "21",
                    "departure_date": "2025-02-23",
                    "departure_time": "22:00:00",
                    "arrival_date": "2025-02-24",
                    "arrival_time": "03:15:00",
                    "duration": "8H15M",
                    "departure_airport": "SYD",
                    "destination_airport": "SIN"
                },
                {
                    "index": 2,
                    "segment_id": 2,
                    "airline_code": "TR",
                    "flight_code": "2",
                    "departure_date": "2025-02-26",
                    "departure_time": "02:00:00",
                    "arrival_date": "2025-02-26",
                    "arrival_time": "13:00:00",
                    "duration": "8H",
                    "departure_airport": "SIN",
                    "destination_airport": "SYD"
                }
            ]
        }
    }'

VIEW:
curl -X 'POST' \
  'http://127.0.0.1:8000/api/flights/get_saved' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user123" 
  }'

UNSAVE:
curl -X 'POST' \
  'http://127.0.0.1:8000/api/flights/unsave' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user123",
    "flight_id": "abc123"
  }'


## Using PostgreSQL database:
To run: psql -h tether-database.postgres.database.azure.com -p 5432 -U tether_postgres_admin postgres
To exit: \q