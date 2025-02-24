## test locally using:
uvicorn app:app --reload

# Creating Docker image
'''
docker pull ghcr.io/gphang/itinerary-app:latest
docker run -d -p 8000:8000 -e OPENWEATHER_KEY="insert_key" -e AMADEUS_KEY="insert_key" -e AMADEUS_SECRET="insert_secret" ghcr.io/gphang/itinerary-app:latest
'''
sample link when docker is running:
http://127.0.0.1:8000/itinerary?city=London&radius=10&limit=2