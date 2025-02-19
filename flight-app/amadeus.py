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


# expired_token = "CFZT9OCmuiZycy5Puazjme83Dvm2"

# # Define the Token Information API URL
# token_info_url = f"https://test.api.amadeus.com/v1/security/oauth2/token/{expired_token}"

# # Make the GET request
# response = requests.get(token_info_url)

# # Check the status of the response
# if response.status_code == 200:
#     token_info = response.json()
#     expires_in = token_info.get('expires_in', None)
#     if expires_in is not None and expires_in < 5:
#         print("The token will expire soon!")
#     else:
#         print("The token is valid.")
# else:
#     print(f"Error: {response.status_code}, {response.text}")