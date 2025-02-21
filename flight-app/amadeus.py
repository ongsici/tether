import requests
import os
from dotenv import load_dotenv

load_dotenv()


url = "https://test.api.amadeus.com/v1/security/oauth2/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials",
    "client_id": os.getenv("AMAD_CLIENT_ID"),
    "client_secret": os.getenv("AMAD_CLIENT_SECRET")
}

response = requests.post(url, headers=headers, data=data)

# Check the response status
if response.status_code == 200:
    print(f"Response: {response}")
    token = response.json().get('access_token')
    print(f"Access token: {token}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
    