<!-- Dockerisation -->
docker buildx build --platform linux/amd64 -t ghcr.io/atchyuni/db-app:latest .
docker push ghcr.io/atchyuni/db-app:latest

# Run app locally
uvicorn src.app:app --reload

# Example save request:
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


## Using PostgreSQL database:
To run: psql -h tether-database.postgres.database.azure.com -p 5432 -U tether_postgres_admin postgres
To exit: \q