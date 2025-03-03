## test locally using:
uvicorn app:app --reload

# Creating Docker image
'''
docker pull ghcr.io/gphang/itinerary-app:latest
docker run -d -p 7000:7000 -e OPENWEATHER_KEY="insert_key" -e AMADEUS_KEY="insert_key" -e AMADEUS_SECRET="insert_secret" ghcr.io/gphang/itinerary-app:latest
'''
sample request when docker is running:
curl -X 'POST' \
  'http://127.0.0.1:7000/itinerary' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "5",
    "itinerary": {
      "city": "London",
      "radius": 10,
      "limit": 5
    }
  }'