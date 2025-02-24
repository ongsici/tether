## test using:
uvicorn app:app --reload

# sample request
curl -X 'POST' \
  'http://127.0.0.1:8000/itinerary' \
  -H 'Content-Type: application/json' \
  -d '{
  "city": "London",
  "radius": 10,
  "limit": 2
}'
