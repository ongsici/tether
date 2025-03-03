import os
import time
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read Amadeus credentials from environment
AMAD_CLIENT_ID = os.getenv("AMAD-CLIENT-ID")
AMAD_CLIENT_SECRET = os.getenv("AMAD-CLIENT-SECRET")

logger = logging.getLogger("flight_microservice")

token = None
token_expiry = 0


def get_amadeus_token() -> str:
    """
    Fetch a new Amadeus access token and store its expiration time.
    Raises requests.exceptions.HTTPError on failure.
    """
    global token, token_expiry

    auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": AMAD_CLIENT_ID,
        "client_secret": AMAD_CLIENT_SECRET
    }

    logger.info("Requesting a new Amadeus access token.")

    try:
        response = requests.post(auth_url, data=payload)
        logger.debug(f"Amadeus token request status code: {response.status_code}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(
            "Failed to retrieve Amadeus token.",
            exc_info=True
        )
        raise

    data = response.json()
    if "access_token" not in data or "expires_in" not in data:
        logger.error(
            f"Amadeus token response is missing expected keys. Response data: {data}"
        )
        raise ValueError("Invalid token response from Amadeus.")

    token = data["access_token"]
    token_expiry = time.time() + data["expires_in"] - 10  # Subtract a buffer for safety

    logger.info("Amadeus access token retrieved successfully.")
    logger.debug(f"Token expires at: {token_expiry} (epoch time)")

    return token


def get_valid_token() -> str:
    """
    Ensure a valid Amadeus token is always used for API requests.
    If the current token is missing or expired, retrieves a new one.
    """
    global token, token_expiry

    if not token or time.time() >= token_expiry:
        logger.info("No valid token found or token has expired. Fetching a new token...")
        return get_amadeus_token()
    else:
        logger.debug("Using existing valid token.")
        return token

    