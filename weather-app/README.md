<!-- instructions for weather-app -->
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
curl -X POST http://127.0.0.1:8000/weather -H "Content-Type: application/json" -d '{"city": "London", "country_code": "GB"}'
