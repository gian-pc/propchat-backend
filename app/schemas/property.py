# app/schemas/property.py
from pydantic import BaseModel
from typing import Optional


class PropertyBase(BaseModel):
    title: str
    price: float
    bedrooms: int
    bathrooms: int
    area: float
    district: str
    type: str
    latitude: float
    longitude: float
    image_url: Optional[str] = None
    description: Optional[str] = None


class PropertyCreate(PropertyBase):
    pass


class Property(PropertyBase):
    id: int

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    properties: Optional[list[Property]] = None