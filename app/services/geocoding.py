"""
Servicio de Geocoding con Mapbox API
Convierte direcciones/lugares a coordenadas geográficas
"""
import httpx
import os
from typing import Optional, Dict
from math import radians, cos, sin, asin, sqrt
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN", "")

# Diccionario de lugares conocidos en Perú (coordenadas exactas)
KNOWN_PLACES = {
    # UTP - Universidad Tecnológica del Perú
    "utp lima centro": {"latitude": -12.0464, "longitude": -77.0428, "name": "UTP Lima Centro"},
    "utp centro": {"latitude": -12.0464, "longitude": -77.0428, "name": "UTP Lima Centro"},
    "utp lima norte": {"latitude": -11.9800, "longitude": -77.0580, "name": "UTP Lima Norte (Los Olivos)"},
    "utp norte": {"latitude": -11.9800, "longitude": -77.0580, "name": "UTP Lima Norte (Los Olivos)"},
    "utp san juan de lurigancho": {"latitude": -11.9876, "longitude": -77.0058, "name": "UTP SJL"},
    "utp sjl": {"latitude": -11.9876, "longitude": -77.0058, "name": "UTP SJL"},
    "utp villa el salvador": {"latitude": -12.2116, "longitude": -76.9364, "name": "UTP VES"},
    "utp ves": {"latitude": -12.2116, "longitude": -76.9364, "name": "UTP VES"},
    "utp ate": {"latitude": -12.0262, "longitude": -76.8971, "name": "UTP Ate"},

    # Parques populares
    "parque kennedy": {"latitude": -12.1211, "longitude": -77.0301, "name": "Parque Kennedy (Miraflores)"},

    # Centros comerciales
    "jockey plaza": {"latitude": -12.0897, "longitude": -76.9777, "name": "Jockey Plaza"},
    "megaplaza": {"latitude": -11.9761, "longitude": -77.0651, "name": "Megaplaza (Los Olivos)"},
}


async def geocode_location(query: str, country: str = "PE") -> Optional[Dict]:
    """
    Convierte un lugar/dirección a coordenadas usando Mapbox Geocoding API

    Args:
        query: Lugar a buscar (ej: "UTP Lima Norte", "Parque Kennedy", "Miraflores")
        country: Código de país ISO (default: PE = Perú)

    Returns:
        {
            "name": "Nombre del lugar",
            "latitude": -12.1234,
            "longitude": -77.5678,
            "place_name": "Nombre completo del lugar"
        }
        o None si no se encuentra
    """
    # 1. Primero buscar en lugares conocidos (más rápido y preciso)
    query_lower = query.lower().strip()
    if query_lower in KNOWN_PLACES:
        place = KNOWN_PLACES[query_lower]
        print(f"✅ Lugar conocido encontrado: {place['name']}")
        return {
            "name": place["name"],
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "place_name": place["name"]
        }

    # 2. Si no está en lugares conocidos, usar Mapbox API
    if not MAPBOX_TOKEN:
        print("WARNING: MAPBOX_TOKEN no configurado")
        return None

    try:
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json"
        params = {
            "access_token": MAPBOX_TOKEN,
            "country": country,
            "limit": 1,
            "language": "es"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        if data.get("features") and len(data["features"]) > 0:
            feature = data["features"][0]
            coords = feature["geometry"]["coordinates"]

            return {
                "name": feature.get("text", query),
                "longitude": coords[0],
                "latitude": coords[1],
                "place_name": feature.get("place_name", query)
            }

        return None

    except Exception as e:
        print(f"Error en geocoding: {e}")
        return None


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia en kilómetros entre dos puntos geográficos
    usando la fórmula de Haversine

    Args:
        lat1, lon1: Coordenadas del primer punto
        lat2, lon2: Coordenadas del segundo punto

    Returns:
        Distancia en kilómetros
    """
    # Convertir a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Fórmula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    # Radio de la Tierra en kilómetros
    r = 6371

    return c * r


def filter_properties_by_distance(
    properties: list,
    center_lat: float,
    center_lng: float,
    radius_km: float = 2.0
) -> list:
    """
    Filtra propiedades dentro de un radio desde un punto central

    Args:
        properties: Lista de propiedades (dicts con latitude, longitude)
        center_lat: Latitud del centro
        center_lng: Longitud del centro
        radius_km: Radio de búsqueda en kilómetros (default: 2 km)

    Returns:
        Lista de propiedades dentro del radio, ordenadas por distancia
    """
    results = []

    for prop in properties:
        if "latitude" not in prop or "longitude" not in prop:
            continue

        distance = haversine_distance(
            center_lat, center_lng,
            prop["latitude"], prop["longitude"]
        )

        if distance <= radius_km:
            # Agregamos la distancia al objeto (útil para ordenar)
            prop_with_distance = {**prop, "distance_km": round(distance, 2)}
            results.append(prop_with_distance)

    # Ordenar por distancia (más cercanas primero)
    results.sort(key=lambda x: x["distance_km"])

    return results
