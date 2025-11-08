# app/models/property.py
from sqlalchemy import Column, Integer, String, Float, Enum
from geoalchemy2 import Geometry
import enum
from app.database import Base


class PropertyType(str, enum.Enum):
    apartment = "apartment"
    house = "house"
    studio = "studio"
    loft = "loft"


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    area = Column(Float, nullable=False)
    district = Column(String, nullable=False)
    type = Column(Enum(PropertyType), nullable=False)
    image_url = Column(String)
    description = Column(String)

    # PostGIS geometry column
    location = Column(Geometry('POINT', srid=4326))

    # Para almacenar lat/lon separado también
    latitude = Column(Float)
    longitude = Column(Float)