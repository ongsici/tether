<!-- testing locally -->
[1] use virtual environment
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt

[2] give execution permission
chmod +x scripts/start.sh

[3] run script
./scripts/start.sh

[4] check if API is running
curl -X POST http://127.0.0.1:8000/weather -H "Content-Type: application/json" -d '{"user_id": "123", "weather": {"city": "London"}}'

[5] if testing as Docker image
docker run -d -p 8000:8000 -e OPENWEATHER_API_KEY={OPENWEATHER_API_KEY} ghcr.io/atchyuni/weather-app:latest
http://0.0.0.0:8000/weather?city=London&country_code=GB

<!-- Dockerisation -->
docker buildx build --platform linux/amd64 -t ghcr.io/atchyuni/weather-app:latest .
docker push ghcr.io/atchyuni/weather-app:latest    
