# Itinerary Microservice

This microservice connects to Azure's PostgreSQL Database Server to perform the following actions:
1. Save a flight (from flight results page)
2. Unsave a flight
3. List all previously saved flights
4. Save an itinerary (from itinerary results page)
5. Unsave an itinerary
6. List all previously saved itineraries


## Website images

![Saved flights](./web_images/saved_flights.png)
![Saved itinerary](./web_images/saved_itinerary.png)


## Endpoints
The API specification can be found here:
[Flight OpenAPI JSON Specification](./docs/openapi.json)


## Local Usage and Development
First create an environment (conda or venv):

```
conda create -n db-handler python=3.10 -y
conda activate db-handler
pip install -r requirements.txt
```


### PostgreSQL usage

How we ran it on Azure (exit anytime using `\q`):

```
psql -h {DB_HOST} -p 5432 -U {DB_USER} {DB_NAME}
```


### Running locally on Uvicorn

From the `db-handler` directory, you can run the app using uvicorn (need database access):

```
uvicorn app:app --reload
```


### Running on Docker

Alternatively, you can run by pulling an existing public Docker image (need database access):

'''
docker pull ghcr.io/gphang/db-app:latest
docker run -d \
  -e DB_HOST="insert_host" \
  -e DB_NAME="your_database_name" \
  -e DB_USER="your_username" \
  -e DB_PASSWORD="your_password" \
  -e DB_PORT=5432 \
  ghcr.io/gphang/db-app:latest
'''


### Example itinerary requests

SAVE:

'''
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
'''

VIEW:

'''
curl -X GET "http://127.0.0.1:8000/api/itineraries/get_saved?user_id=user12345"
'''

UNSAVE:

'''
Here is a sample itinerary unsave request:
curl -X 'POST' \
  'http://127.0.0.1:8000/api/itineraries/unsave' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "12345",
    "activity_id": "abc123"
  }'
'''

### Example flight requests

SAVE:

'''
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
'''

VIEW:

'''
curl -X GET "http://127.0.0.1:8000/api/flights/get_saved?user_id=user123"
'''

UNSAVE:

'''
curl -X 'POST' \
  'http://127.0.0.1:8000/api/flights/unsave' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "123",
    "flight_id": "XYZ123"
  }'
'''