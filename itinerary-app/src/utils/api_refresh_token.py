import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()  # Load API credentials from .env

# Amadeus API credentials
AMADEUS_KEY = os.getenv("AMADEUS-KEY")
AMADEUS_SECRET = os.getenv("AMADEUS-SECRET")

# Global storage for token and expiry time
token = None
token_expiry = 0  # Stores expiration timestamp


def get_amadeus_token():
    """Fetch a new Amadeus access token and store its expiration time."""
    global token, token_expiry

    auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_KEY,
        "client_secret": AMADEUS_SECRET
    }

    response = requests.post(auth_url, data=payload)
    response.raise_for_status()  # Raise error if request fails

    data = response.json()
    token = data["access_token"]
    token_expiry = time.time() + data["expires_in"] - 10  # Subtract 10s buffer for safety

    return token


def get_valid_token():
    """Ensure a valid Amadeus token is always used for API requests."""
    if not token or time.time() >= token_expiry:
        return get_amadeus_token()
    return token
