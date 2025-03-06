# Weather Microservice

This microservice uses two APIs:
1. OpenWeather: gets weather data
2. Open-Meteo: gets weather forecast

## Website images

![Weather search](./web_images/weather_search.png)
![Weather results](./web_images/weather_results.png)


## Endpoints
The API specification can be found here:
[Weather OpenAPI JSON Specification](./docs/openapi.json)

## Local Usage and Development
First create an environment (conda or venv):

```
conda create -n weather python=3.10 -y
conda activate weather
pip install -r requirements.txt
```


### Running locally on Uvicorn

From the `weather-app` directory, you can run the app using uvicorn:

```
uvicorn app:app --reload
```


### Running on Docker
Alternatively, you can run by pulling an existing public Docker image:

'''
docker pull ghcr.io/atchyuni/weather-app:latest
docker run -d -p 8000:8000 -e OPENWEATHER_API_KEY="insert_key" ghcr.io/atchyuni/weather-app:latest
'''

Here is a sample request when docker is running:
curl -X 'POST' \
  'http://127.0.0.1:8000/weather' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "5",
    "weather": {
      "city": "London"
    }
  }'