from pydantic import BaseModel
from typing import List, Optional


# request model for endpoint
class ItineraryRequestObj(BaseModel):
    city: str
    radius: int
    limit: int

class ItineraryRequest(BaseModel):
    user_id: str
    itinerary: ItineraryRequestObj

# response model for endpoint
class ItineraryResponseObj(BaseModel):
    city: str
    activity_id: str
    activity_name: str
    activity_details: str
    price_amount: str
    price_currency: str
    pictures: List[str]

class ItineraryResponse(BaseModel):
    user_id: str
    results: List[ItineraryResponseObj]