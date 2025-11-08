from fastapi import APIRouter

router = APIRouter(prefix="/api/properties", tags=["properties"])

# Mock data
MOCK_PROPERTIES = [
    {
        "id": "1",
        "title": "Acogedor departamento en Miraflores",
        "price": 1200,
        "bedrooms": 2,
        "bathrooms": 1,
        "area": 80,
        "district": "Miraflores",
        "latitude": -12.1198,
        "longitude": -77.0289,
        "imageUrl": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400",
        "type": "apartment"
    },
    {
        "id": "2",
        "title": "Casa moderna en San Isidro",
        "price": 2500,
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 150,
        "district": "San Isidro",
        "latitude": -12.0969,
        "longitude": -77.0347,
        "imageUrl": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400",
        "type": "house"
    },
    {
        "id": "3",
        "title": "Departamento frente al mar - Barranco",
        "price": 1800,
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 95,
        "district": "Barranco",
        "latitude": -12.1467,
        "longitude": -77.0208,
        "imageUrl": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
        "type": "apartment"
    }
]

@router.get("")
async def get_properties():
    """Get all properties"""
    return {
        "properties": MOCK_PROPERTIES,
        "total": len(MOCK_PROPERTIES)
    }

@router.get("/{property_id}")
async def get_property(property_id: str):
    """Get property by ID"""
    prop = next((p for p in MOCK_PROPERTIES if p["id"] == property_id), None)
    if not prop:
        return {"error": "Property not found"}, 404
    return {"property": prop}