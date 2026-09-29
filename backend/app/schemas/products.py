from typing import Optional
from pydantic import BaseModel, ConfigDict

# & Basic product schema that matches the product table in the DB using pydantic lib
class Products_Base(BaseModel):
    title: str
    author: str
    genre: str
    release_date: Optional[int] = None
    rating: Optional[float] = None
    price: float
    stock: int = 0
    image: Optional[str] = None
    description: Optional[str] = None
# ! the response that will pass its value to the router 
class Products_Response(Products_Base):
    id: int

    model_config = ConfigDict(from_attributes=True)
