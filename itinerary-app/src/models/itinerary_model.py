from pydantic import BaseModel
from typing import List, Optional


# request model for endpoint
class ItineraryRequest(BaseModel):
    city: str
    radius: int
    limit: int

# response model for endpoint
class ItineraryResponse(BaseModel):
    city: str
    activity_id: str
    activity_name: str
    activity_details: str
    price_amount: str
    price_currency: str
    pictures: List[str]
