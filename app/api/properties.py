from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from ..services.geocoding import geocode_location, filter_properties_by_distance
from ..data.mock_properties import MOCK_PROPERTIES

router = APIRouter(prefix="/api/properties", tags=["properties"])


# === ENDPOINTS ===

@router.get("")
async def get_properties(
        district: Optional[str] = None,
        department: Optional[str] = None,
        near: Optional[str] = None,  # Nuevo: lugar de referencia
        radius_km: Optional[float] = Query(2.0, alias="radius_km"),  # Radio de búsqueda en km
        min_price: Optional[float] = Query(None, alias="min_price"),
        max_price: Optional[float] = Query(None, alias="max_price"),
        bedrooms: Optional[int] = None,
        property_type: Optional[str] = Query(None, alias="property_type"),
        transaction_type: Optional[str] = Query(None, alias="transaction_type")
):
    """
    Get all properties with optional filters

    New: Supports geospatial search with 'near' parameter
    Example: /api/properties?near=UTP%20Lima%20Norte&radius_km=2
    """

    # Empezamos con la lista completa
    filtered_properties = MOCK_PROPERTIES

    # 1. FILTRO GEOESPACIAL (si hay "near")
    if near:
        print(f"🔍 Geocoding: '{near}'")
        location = await geocode_location(near, country="PE")

        if location:
            print(f"✅ Encontrado: {location['place_name']} ({location['latitude']}, {location['longitude']})")
            # Filtrar propiedades dentro del radio
            filtered_properties = filter_properties_by_distance(
                filtered_properties,
                location['latitude'],
                location['longitude'],
                radius_km
            )
            print(f"📍 Encontradas {len(filtered_properties)} propiedades dentro de {radius_km}km")
        else:
            print(f"❌ No se pudo geocodificar: '{near}'")
            # Si no se puede geocodificar, retornar lista vacía
            return {"properties": [], "total": 0}

    # 2. FILTROS TRADICIONALES
    if department:
        filtered_properties = [p for p in filtered_properties if
                               p.get('department') and p['department'].upper() == department.upper()]

    if district:
        filtered_properties = [p for p in filtered_properties if
                               p.get('district') and p['district'].lower() == district.lower()]

    if min_price is not None:
        filtered_properties = [p for p in filtered_properties if p.get('price') is not None and p['price'] >= min_price]

    if max_price is not None:
        filtered_properties = [p for p in filtered_properties if p.get('price') is not None and p['price'] <= max_price]

    if bedrooms is not None:
        # Asumimos que bedrooms=2 significa 2 o más
        filtered_properties = [p for p in filtered_properties if
                               p.get('bedrooms') is not None and p['bedrooms'] >= bedrooms]

    if property_type:
        filtered_properties = [p for p in filtered_properties if
                               p.get('type') and p['type'].lower() == property_type.lower()]

    if transaction_type:
        filtered_properties = [p for p in filtered_properties if
                               p.get('transaction_type') and p['transaction_type'].lower() == transaction_type.lower()]

    return {
        "properties": filtered_properties,
        "total": len(filtered_properties)
    }


@router.get("/{property_id}")
async def get_property(property_id: str):
    """Get property by ID"""
    prop = next((p for p in MOCK_PROPERTIES if p["id"] == property_id), None)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"property": prop}