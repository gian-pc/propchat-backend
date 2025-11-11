from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/properties", tags=["properties"])

# --- ¡NUEVOS MOCK DATA! (Más de 120+ propiedades) ---
# He añadido 'transaction_type' (rent/sale) a todas
MOCK_PROPERTIES = [
    # --- LIMA (5) ---
    {
        "id": "1", "title": "Acogedor depa en Miraflores", "price": 1200, "bedrooms": 2, "bathrooms": 1, "area": 80,
        "district": "Miraflores", "latitude": -12.1198, "longitude": -77.0289,
        "imageUrl": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400",
        "type": "apartment", "department": "LIMA", "transaction_type": "rent"
    },
    {
        "id": "2", "title": "Casa moderna en San Isidro", "price": 2500, "bedrooms": 3, "bathrooms": 2, "area": 150,
        "district": "San Isidro", "latitude": -12.0969, "longitude": -77.0347,
        "imageUrl": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400",
        "type": "house", "department": "LIMA", "transaction_type": "rent"
    },
    {
        "id": "3", "title": "Depa frente al mar - Barranco", "price": 1800, "bedrooms": 2, "bathrooms": 2, "area": 95,
        "district": "Barranco", "latitude": -12.1467, "longitude": -77.0208,
        "imageUrl": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
        "type": "apartment", "department": "LIMA", "transaction_type": "rent"
    },
    {
        "id": "100", "title": "Terreno en Cieneguilla", "price": 75000, "bedrooms": 0, "bathrooms": 0, "area": 1000,
        "district": "Cieneguilla", "latitude": -12.1080, "longitude": -76.7840,
        "imageUrl": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=400",
        "type": "house", "department": "LIMA", "transaction_type": "sale"  # Terreno
    },
    {
        "id": "101", "title": "Casa de campo en Chosica", "price": 1300, "bedrooms": 4, "bathrooms": 3, "area": 300,
        "district": "Chosica", "latitude": -11.9370, "longitude": -76.6900,
        "imageUrl": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=400",
        "type": "house", "department": "LIMA", "transaction_type": "rent"
    },

    # --- AREQUIPA (5) ---
    {
        "id": "4", "title": "Bello depa en Yanahuara", "price": 900, "bedrooms": 2, "bathrooms": 1, "area": 70,
        "district": "Yanahuara", "latitude": -16.3888, "longitude": -71.5421,
        "imageUrl": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400",
        "type": "apartment", "department": "AREQUIPA", "transaction_type": "rent"
    },
    {
        "id": "5", "title": "Casa grande en Cayma", "price": 1500, "bedrooms": 4, "bathrooms": 3, "area": 200,
        "district": "Cayma", "latitude": -16.3770, "longitude": -71.5340,
        "imageUrl": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400",
        "type": "house", "department": "AREQUIPA", "transaction_type": "rent"
    },
    {
        "id": "6", "title": "Mini depa cerca al centro", "price": 700, "bedrooms": 1, "bathrooms": 1, "area": 45,
        "district": "Cercado", "latitude": -16.4010, "longitude": -71.5365,
        "imageUrl": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400",
        "type": "apartment", "department": "AREQUIPA", "transaction_type": "rent"
    },
    {
        "id": "7", "title": "Terreno amplio en Socabaya", "price": 50000, "bedrooms": 0, "bathrooms": 0, "area": 500,
        "district": "Socabaya", "latitude": -16.4490, "longitude": -71.5230,
        "imageUrl": "https://images.unsplash.com/photo-1506765515386-0a8e03639e4b?w=400",
        "type": "house", "department": "AREQUIPA", "transaction_type": "sale"
    },
    {
        "id": "8", "title": "Depa con vista al Misti", "price": 1100, "bedrooms": 3, "bathrooms": 2, "area": 100,
        "district": "Jose Luis Bustamante", "latitude": -16.4270, "longitude": -71.5200,
        "imageUrl": "https://images.unsplash.com/photo-1505691938895-1758d7FEB511?w=400",
        "type": "apartment", "department": "AREQUIPA", "transaction_type": "rent"
    },

    # --- CUSCO (5) ---
    {
        "id": "9", "title": "Habitación cerca a Plaza de Armas", "price": 500, "bedrooms": 1, "bathrooms": 1,
        "area": 30,
        "district": "Cercado", "latitude": -13.5170, "longitude": -71.9785,
        "imageUrl": "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=400",
        "type": "apartment", "department": "CUSCO", "transaction_type": "rent"
    },
    {
        "id": "10", "title": "Casa de campo en Valle Sagrado", "price": 2200, "bedrooms": 3, "bathrooms": 2,
        "area": 180,
        "district": "Urubamba", "latitude": -13.3050, "longitude": -72.1150,
        "imageUrl": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=400",
        "type": "house", "department": "CUSCO", "transaction_type": "rent"
    },
    {
        "id": "11", "title": "Depa moderno en Wanchaq", "price": 850, "bedrooms": 2, "bathrooms": 1, "area": 65,
        "district": "Wanchaq", "latitude": -13.5250, "longitude": -71.9650,
        "imageUrl": "https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=400",
        "type": "apartment", "department": "CUSCO", "transaction_type": "rent"
    },
    {
        "id": "12", "title": "Local comercial en San Sebastian", "price": 1300, "bedrooms": 0, "bathrooms": 1,
        "area": 90,
        "district": "San Sebastian", "latitude": -13.5350, "longitude": -71.9200,
        "imageUrl": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400",
        "type": "house", "department": "CUSCO", "transaction_type": "rent"
    },
    {
        "id": "13", "title": "Terreno en venta - Pisac", "price": 100000, "bedrooms": 0, "bathrooms": 0, "area": 500,
        "district": "Pisac", "latitude": -13.4220, "longitude": -71.8480,
        "imageUrl": "https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=400",
        "type": "house", "department": "CUSCO", "transaction_type": "sale"
    },

    # --- LORETO (5) ---
    {
        "id": "14", "title": "Casa con piscina en Iquitos", "price": 1900, "bedrooms": 3, "bathrooms": 2, "area": 160,
        "district": "Iquitos", "latitude": -3.7490, "longitude": -73.2538,
        "imageUrl": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400",
        "type": "house", "department": "LORETO", "transaction_type": "rent"
    },
    {
        "id": "15", "title": "Depa céntrico en Iquitos", "price": 750, "bedrooms": 2, "bathrooms": 1, "area": 60,
        "district": "Iquitos", "latitude": -3.7430, "longitude": -73.2490,
        "imageUrl": "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=400",
        "type": "apartment", "department": "LORETO", "transaction_type": "rent"
    },
    {
        "id": "16", "title": "Casa en Punchana", "price": 1000, "bedrooms": 3, "bathrooms": 1, "area": 110,
        "district": "Punchana", "latitude": -3.7250, "longitude": -73.2450,
        "imageUrl": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400",
        "type": "house", "department": "LORETO", "transaction_type": "rent"
    },
    {
        "id": "17", "title": "Depa en Belen", "price": 600, "bedrooms": 2, "bathrooms": 1, "area": 55,
        "district": "Belen", "latitude": -3.7650, "longitude": -73.2550,
        "imageUrl": "https://images.unsplash.com/photo-1533779283484-8ad4940aa3a8?w=400",
        "type": "apartment", "department": "LORETO", "transaction_type": "rent"
    },
    {
        "id": "18", "title": "Terreno en venta Iquitos", "price": 30000, "bedrooms": 0, "bathrooms": 0, "area": 1000,
        "district": "Iquitos", "latitude": -3.7700, "longitude": -73.2600,
        "imageUrl": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=400",
        "type": "house", "department": "LORETO", "transaction_type": "sale"
    },

    # --- PIURA (5) ---
    {
        "id": "19", "title": "Casa de playa en Mancora", "price": 2800, "bedrooms": 4, "bathrooms": 3, "area": 220,
        "district": "Mancora", "latitude": -4.1060, "longitude": -81.0480,
        "imageUrl": "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=400",
        "type": "house", "department": "PIURA", "transaction_type": "rent"
    },
    {
        "id": "20", "title": "Depa en Piura Centro", "price": 800, "bedrooms": 2, "bathrooms": 1, "area": 70,
        "district": "Piura", "latitude": -5.1945, "longitude": -80.6328,
        "imageUrl": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=400",
        "type": "apartment", "department": "PIURA", "transaction_type": "rent"
    },
    {
        "id": "21", "title": "Casa en Catacaos", "price": 1100, "bedrooms": 3, "bathrooms": 2, "area": 130,
        "district": "Catacaos", "latitude": -5.2710, "longitude": -80.6810,
        "imageUrl": "https://images.unsplash.com/photo-1598228723793-52759bba239c?w=400",
        "type": "house", "department": "PIURA", "transaction_type": "rent"
    },
    {
        "id": "22", "title": "Depa en Urb. Miraflores (Piura)", "price": 950, "bedrooms": 3, "bathrooms": 2, "area": 90,
        "district": "Castilla", "latitude": -5.1850, "longitude": -80.6200,
        "imageUrl": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400",
        "type": "apartment", "department": "PIURA", "transaction_type": "rent"
    },
    {
        "id": "23", "title": "Terreno en Sullana", "price": 45000, "bedrooms": 0, "bathrooms": 0, "area": 100,
        "district": "Sullana", "latitude": -4.9040, "longitude": -80.6860,
        "imageUrl": "https://images.unsplash.com/photo-1513584684374-8bab748fbf90?w=400",
        "type": "house", "department": "PIURA", "transaction_type": "sale"
    },

    # --- AMAZONAS (5) ---
    {
        "id": "24", "title": "Casa en Chachapoyas", "price": 800, "bedrooms": 3, "bathrooms": 1, "area": 120,
        "district": "Chachapoyas", "latitude": -6.2280, "longitude": -77.8680,
        "imageUrl": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400",
        "type": "house", "department": "AMAZONAS", "transaction_type": "rent"
    },
    {
        "id": "25", "title": "Depa con vista", "price": 600, "bedrooms": 2, "bathrooms": 1, "area": 60,
        "district": "Chachapoyas", "latitude": -6.2310, "longitude": -77.8700,
        "imageUrl": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400",
        "type": "apartment", "department": "AMAZONAS", "transaction_type": "rent"
    },
    {
        "id": "26", "title": "Terreno en Bagua Grande", "price": 25000, "bedrooms": 0, "bathrooms": 0, "area": 300,
        "district": "Bagua Grande", "latitude": -5.7590, "longitude": -78.4350,
        "imageUrl": "https://images.unsplash.com/photo-1506765515386-0a8e03639e4b?w=400",
        "type": "house", "department": "AMAZONAS", "transaction_type": "sale"
    },
    {
        "id": "27", "title": "Casa de campo - Rodriguez de Mendoza", "price": 1100, "bedrooms": 3, "bathrooms": 2,
        "area": 150,
        "district": "Mendoza", "latitude": -6.3950, "longitude": -77.4850,
        "imageUrl": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400",
        "type": "house", "department": "AMAZONAS", "transaction_type": "rent"
    },
    {
        "id": "28", "title": "Depa en Bagua", "price": 500, "bedrooms": 2, "bathrooms": 1, "area": 50,
        "district": "Bagua", "latitude": -5.6400, "longitude": -78.5300,
        "imageUrl": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
        "type": "apartment", "department": "AMAZONAS", "transaction_type": "rent"
    },

    # --- ANCASH (5) ---
    {
        "id": "29", "title": "Depa en Huaraz", "price": 700, "bedrooms": 2, "bathrooms": 1, "area": 65,
        "district": "Huaraz", "latitude": -9.5260, "longitude": -77.5280,
        "imageUrl": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400",
        "type": "apartment", "department": "ANCASH", "transaction_type": "rent"
    },
    {
        "id": "30", "title": "Casa en Chimbote", "price": 1200, "bedrooms": 3, "bathrooms": 2, "area": 130,
        "district": "Chimbote", "latitude": -9.0800, "longitude": -78.5800,
        "imageUrl": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400",
        "type": "house", "department": "ANCASH", "transaction_type": "rent"
    },
    {
        "id": "31", "title": "Terreno en Caraz", "price": 35000, "bedrooms": 0, "bathrooms": 0, "area": 400,
        "district": "Caraz", "latitude": -9.0480, "longitude": -77.8100,
        "imageUrl": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=400",
        "type": "house", "department": "ANCASH", "transaction_type": "sale"
    },
    {
        "id": "32", "title": "Depa amoblado Huaraz", "price": 900, "bedrooms": 1, "bathrooms": 1, "area": 50,
        "district": "Huaraz", "latitude": -9.5300, "longitude": -77.5300,
        "imageUrl": "https://images.unsplash.com/photo-1505691938895-1758d7FEB511?w=400",
        "type": "apartment", "department": "ANCASH", "transaction_type": "rent"
    },
    {
        "id": "33", "title": "Casa de playa en Casma", "price": 1800, "bedrooms": 3, "bathrooms": 2, "area": 140,
        "district": "Casma", "latitude": -9.4710, "longitude": -78.3150,
        "imageUrl": "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=400",
        "type": "house", "department": "ANCASH", "transaction_type": "rent"
    },

    # --- APURIMAC (5) ---
    {
        "id": "34", "title": "Depa en Abancay", "price": 650, "bedrooms": 2, "bathrooms": 1, "area": 70,
        "district": "Abancay", "latitude": -13.6330, "longitude": -72.8810,
        "imageUrl": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400",
        "type": "apartment", "department": "APURIMAC", "transaction_type": "rent"
    },
    {
        "id": "35", "title": "Casa en Andahuaylas", "price": 900, "bedrooms": 3, "bathrooms": 2, "area": 120,
        "district": "Andahuaylas", "latitude": -13.6570, "longitude": -73.3860,
        "imageUrl": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400",
        "type": "house", "department": "APURIMAC", "transaction_type": "rent"
    },
    {
        "id": "36", "title": "Terreno en Abancay", "price": 40000, "bedrooms": 0, "bathrooms": 0, "area": 300,
        "district": "Abancay", "latitude": -13.6380, "longitude": -72.8750,
        "imageUrl": "https://images.unsplash.com/photo-1506765515386-0a8e03639e4b?w=400",
        "type": "house", "department": "APURIMAC", "transaction_type": "sale"
    },
    {
        "id": "37", "title": "Depa céntrico Andahuaylas", "price": 500, "bedrooms": 1, "bathrooms": 1, "area": 45,
        "district": "Andahuaylas", "latitude": -13.6600, "longitude": -73.3800,
        "imageUrl": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400",
        "type": "apartment", "department": "APURIMAC", "transaction_type": "rent"
    },
    {
        "id": "38", "title": "Casa amoblada Abancay", "price": 1000, "bedrooms": 3, "bathrooms": 1, "area": 110,
        "district": "Abancay", "latitude": -13.6300, "longitude": -72.8800,
        "imageUrl": "https://images.unsplash.com/photo-1598228723793-52759bba239c?w=400",
        "type": "house", "department": "APURIMAC", "transaction_type": "rent"
    },

    # --- AYACUCHO (5) ---
    {
        "id": "39", "title": "Depa colonial en Huamanga", "price": 800, "bedrooms": 2, "bathrooms": 1, "area": 75,
        "district": "Ayacucho", "latitude": -13.1580, "longitude": -74.2230,
        "imageUrl": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
        "type": "apartment", "department": "AYACUCHO", "transaction_type": "rent"
    },
    {
        "id": "40", "title": "Casa en Huanta", "price": 950, "bedrooms": 3, "bathrooms": 2, "area": 130,
        "district": "Huanta", "latitude": -12.9370, "longitude": -74.2480,
        "imageUrl": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400",
        "type": "house", "department": "AYACUCHO", "transaction_type": "rent"
    },
    {
        "id": "41", "title": "Terreno en venta - Huamanga", "price": 60000, "bedrooms": 0, "bathrooms": 0, "area": 500,
        "district": "Ayacucho", "latitude": -13.1650, "longitude": -74.2200,
        "imageUrl": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=400",
        "type": "house", "department": "AYACUCHO", "transaction_type": "sale"
    },
    {
        "id": "42", "title": "Depa moderno Ayacucho", "price": 700, "bedrooms": 2, "bathrooms": 1, "area": 60,
        "district": "Ayacucho", "latitude": -13.1600, "longitude": -74.2250,
        "imageUrl": "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=400",
        "type": "apartment", "department": "AYACUCHO", "transaction_type": "rent"
    },
    {
        "id": "43", "title": "Casa de campo en Quinua", "price": 1100, "bedrooms": 3, "bathrooms": 1, "area": 150,
        "district": "Quinua", "latitude": -13.0600, "longitude": -74.1350,
        "imageUrl": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400",
        "type": "house", "department": "AYACUCHO", "transaction_type": "rent"
    },

    # --- CAJAMARCA (5) ---
    {
        "id": "44", "title": "Depa con vista al Cumbe Mayo", "price": 750, "bedrooms": 2, "bathrooms": 1, "area": 70,
        "district": "Cajamarca", "latitude": -7.1630, "longitude": -78.5130,
        "imageUrl": "https://images.unsplash.com/photo-1533779283484-8ad4940aa3a8?w=400",
        "type": "apartment", "department": "CAJAMARCA", "transaction_type": "rent"
    },
    {
        "id": "45", "title": "Casa en Jaen", "price": 1000, "bedrooms": 3, "bathrooms": 2, "area": 120,
        "district": "Jaen", "latitude": -5.7080, "longitude": -78.8080,
        "imageUrl": "https://images.unsplash.com/photo-1505873242700-f289a29e1e0f?w=400",
        "type": "house", "department": "CAJAMARCA", "transaction_type": "rent"
    },
    {
        "id": "46", "title": "Terreno en Baños del Inca", "price": 80000, "bedrooms": 0, "bathrooms": 0, "area": 600,
        "district": "Baños del Inca", "latitude": -7.1450, "longitude": -78.4600,
        "imageUrl": "https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=400",
        "type": "house", "department": "CAJAMARCA", "transaction_type": "sale"
    },
    {
        "id": "47", "title": "Mini depa en Cajamarca", "price": 550, "bedrooms": 1, "bathrooms": 1, "area": 40,
        "district": "Cajamarca", "latitude": -7.1600, "longitude": -78.5100,
        "imageUrl": "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=400",
        "type": "apartment", "department": "CAJAMARCA", "transaction_type": "rent"
    },
    {
        "id": "48", "title": "Casa en Chota", "price": 850, "bedrooms": 3, "bathrooms": 1, "area": 110,
        "district": "Chota", "latitude": -6.5600, "longitude": -78.6500,
        "imageUrl": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=400",
        "type": "house", "department": "CAJAMARCA", "transaction_type": "rent"
    },

    # --- CALLAO (5) ---
    {
        "id": "49", "title": "Depa en La Punta", "price": 1300, "bedrooms": 2, "bathrooms": 2, "area": 85,
        "district": "La Punta", "latitude": -12.0720, "longitude": -77.1580,
        "imageUrl": "https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=400",
        "type": "apartment", "department": "CALLAO", "transaction_type": "rent"
    },
    {
        "id": "50", "title": "Casa en Bellavista", "price": 1600, "bedrooms": 3, "bathrooms": 2, "area": 140,
        "district": "Bellavista", "latitude": -12.0580, "longitude": -77.1280,
        "imageUrl": "https://images.unsplash.com/photo-1513584684374-8bab748fbf90?w=400",
        "type": "house", "department": "CALLAO", "transaction_type": "rent"
    },
    {
        "id": "51", "title": "Depa en La Perla", "price": 900, "bedrooms": 2, "bathrooms": 1, "area": 65,
        "district": "La Perla", "latitude": -12.0650, "longitude": -77.1350,
        "imageUrl": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400",
        "type": "apartment", "department": "CALLAO", "transaction_type": "rent"
    },
    {
        "id": "52", "title": "Almacén en Venta - Callao", "price": 250000, "bedrooms": 0, "bathrooms": 2, "area": 1000,
        "district": "Callao", "latitude": -12.0500, "longitude": -77.1400,
        "imageUrl": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400",
        "type": "house", "department": "CALLAO", "transaction_type": "sale"
    },
    {
        "id": "53", "title": "Depa en Carmen de La Legua", "price": 750, "bedrooms": 3, "bathrooms": 1, "area": 75,
        "district": "Carmen de La Legua", "latitude": -12.0450, "longitude": -77.1050,
        "imageUrl": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=400",
        "type": "apartment", "department": "CALLAO", "transaction_type": "rent"
    },

    # --- HUANCAVELICA (5) ---
    {
        "id": "54", "title": "Casa en Huancavelica", "price": 600, "bedrooms": 3, "bathrooms": 1, "area": 100,
        "district": "Huancavelica", "latitude": -12.7860, "longitude": -74.9750,
        "imageUrl": "https://images.unsplash.com/photo-1598228723793-52759bba239c?w=400",
        "type": "house", "department": "HUANCAVELICA", "transaction_type": "rent"
    },
    {
        "id": "55", "title": "Depa en Lircay", "price": 450, "bedrooms": 2, "bathrooms": 1, "area": 60,
        "district": "Lircay", "latitude": -12.9880, "longitude": -74.7200,
        "imageUrl": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
        "type": "apartment", "department": "HUANCAVELICA", "transaction_type": "rent"
    },
    {
        "id": "56", "title": "Terreno en Acobamba", "price": 20000, "bedrooms": 0, "bathrooms": 0, "area": 300,
        "district": "Acobamba", "latitude": -12.8400, "longitude": -74.5680,
        "imageUrl": "https://images.unsplash.com/photo-1506765515386-0a8e03639e4b?w=400",
        "type": "house", "department": "HUANCAVELICA", "transaction_type": "sale"
    },
    {
        "id": "57", "title": "Casa céntrica Huancavelica", "price": 700, "bedrooms": 2, "bathrooms": 1, "area": 80,
        "district": "Huancavelica", "latitude": -12.7880, "longitude": -74.9780,
        "imageUrl": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400",
        "type": "house", "department": "HUANCAVELICA", "transaction_type": "rent"
    },
    {
        "id": "58", "title": "Depa pequeño", "price": 400, "bedrooms": 1, "bathrooms": 1, "area": 40,
        "district": "Huancavelica", "latitude": -12.7850, "longitude": -74.9700,
        "imageUrl": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400",
        "type": "apartment", "department": "HUANCAVELICA", "transaction_type": "rent"
    },

    # --- HUANUCO (5) ---
    {
        "id": "59", "title": "Depa en Huanuco", "price": 600, "bedrooms": 2, "bathrooms": 1, "area": 65,
        "district": "Huanuco", "latitude": -9.9300, "longitude": -76.2400,
        "imageUrl": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400",
        "type": "apartment", "department": "HUANUCO", "transaction_type": "rent"
    },
    {
        "id": "60", "title": "Casa en Tingo Maria", "price": 900, "bedrooms": 3, "bathrooms": 2, "area": 120,
        "district": "Tingo Maria", "latitude": -9.2950, "longitude": -75.9980,
        "imageUrl": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400",
        "type": "house", "department": "HUANUCO", "transaction_type": "rent"
    },
    {
        "id": "61", "title": "Terreno en Ambo", "price": 28000, "bedrooms": 0, "bathrooms": 0, "area": 350,
        "district": "Ambo", "latitude": -10.1280, "longitude": -76.2050,
        "imageUrl": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=400",
        "type": "house", "department": "HUANUCO", "transaction_type": "sale"
    },
    {
        "id": "62", "title": "Depa con balcón Huanuco", "price": 750, "bedrooms": 3, "bathrooms": 1, "area": 80,
        "district": "Huanuco", "latitude": -9.9320, "longitude": -76.2430,
        "imageUrl": "https://images.unsplash.com/photo-1505691938895-1758d7FEB511?w=400",
        "type": "apartment", "department": "HUANUCO", "transaction_type": "rent"
    },
    {
        "id": "63", "title": "Casa céntrica Tingo Maria", "price": 1100, "bedrooms": 2, "bathrooms": 2, "area": 100,
        "district": "Tingo Maria", "latitude": -9.2900, "longitude": -76.0000,
        "imageUrl": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=400",
        "type": "house", "department": "HUANUCO", "transaction_type": "rent"
    },

    # --- ICA (5) ---
    {
        "id": "64", "title": "Casa de playa en Paracas", "price": 2200, "bedrooms": 3, "bathrooms": 3, "area": 180,
        "district": "Paracas", "latitude": -13.8350, "longitude": -76.2500,
        "imageUrl": "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=400",
        "type": "house", "department": "ICA", "transaction_type": "rent"
    },
    {
        "id": "65", "title": "Depa en Ica", "price": 800, "bedrooms": 2, "bathrooms": 1, "area": 70,
        "district": "Ica", "latitude": -14.0670, "longitude": -75.7280,
        "imageUrl": "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=400",
        "type": "apartment", "department": "ICA", "transaction_type": "rent"
    },
    {
        "id": "66", "title": "Terreno en Pisco", "price": 50000, "bedrooms": 0, "bathrooms": 0, "area": 400,
        "district": "Pisco", "latitude": -13.7100, "longitude": -76.2050,
        "imageUrl": "https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=400",
        "type": "house", "department": "ICA", "transaction_type": "sale"
    },
    {
        "id": "67", "title": "Casa en Chincha", "price": 1000, "bedrooms": 3, "bathrooms": 2, "area": 130,
        "district": "Chincha", "latitude": -13.4180, "longitude": -76.1330,
        "imageUrl": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400",
        "type": "house", "department": "ICA", "transaction_type": "rent"
    },
    {
        "id": "68", "title": "Depa en Nazca", "price": 600, "bedrooms": 2, "bathrooms": 1, "area": 60,
        "district": "Nazca", "latitude": -14.8330, "longitude": -74.9380,
        "imageUrl": "https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=400",
        "type": "apartment", "department": "ICA", "transaction_type": "rent"
    },

    # --- JUNIN (5) ---
    {
        "id": "69", "title": "Depa en Huancayo", "price": 700, "bedrooms": 2, "bathrooms": 1, "area": 65,
        "district": "Huancayo", "latitude": -12.0650, "longitude": -75.2040,
        "imageUrl": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400",
        "type": "apartment", "department": "JUNIN", "transaction_type": "rent"
    },
    {
        "id": "70", "title": "Casa en Tarma", "price": 900, "bedrooms": 3, "bathrooms": 1, "area": 110,
        "district": "Tarma", "latitude": -11.4180, "longitude": -75.6900,
        "imageUrl": "https://images.unsplash.com/photo-1513584684374-8bab748fbf90?w=400",
        "type": "house", "department": "JUNIN", "transaction_type": "rent"
    },
    {
        "id": "71", "title": "Terreno en La Merced", "price": 45000, "bedrooms": 0, "bathrooms": 0, "area": 500,
        "district": "La Merced", "latitude": -11.0600, "longitude": -75.3300,
        "imageUrl": "https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=400",
        "type": "house", "department": "JUNIN", "transaction_type": "sale"
    },
    {
        "id": "72", "title": "Depa céntrico Huancayo", "price": 850, "bedrooms": 3, "bathrooms": 2, "area": 80,
        "district": "Huancayo", "latitude": -12.0700, "longitude": -75.2100,
        "imageUrl": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=400",
        "type": "apartment", "department": "JUNIN", "transaction_type": "rent"
    },
    {
        "id": "73", "title": "Casa de campo en Jauja", "price": 1200, "bedrooms": 3, "bathrooms": 2, "area": 150,
        "district": "Jauja", "latitude": -11.7750, "longitude": -75.4980,
        "imageUrl": "https://images.unsplash.com/photo-1598228723793-52759bba239c?w=400",
        "type": "house", "department": "JUNIN", "transaction_type": "rent"
    },

    # --- LA LIBERTAD (5) ---
    {
        "id": "74", "title": "Depa en Trujillo", "price": 850, "bedrooms": 2, "bathrooms": 1, "area": 70,
        "district": "Trujillo", "latitude": -8.1110, "longitude": -79.0280,
        "imageUrl": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
        "type": "apartment", "department": "LA LIBERTAD", "transaction_type": "rent"
    },
    {
        "id": "75", "title": "Casa de playa en Huanchaco", "price": 1900, "bedrooms": 3, "bathrooms": 2, "area": 140,
        "district": "Huanchaco", "latitude": -8.0780, "longitude": -79.1200,
        "imageUrl": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400",
        "type": "house", "department": "LA LIBERTAD", "transaction_type": "rent"
    },
    {
        "id": "76", "title": "Terreno en Pacasmayo", "price": 60000, "bedrooms": 0, "bathrooms": 0, "area": 500,
        "district": "Pacasmayo", "latitude": -7.4000, "longitude": -79.5700,
        "imageUrl": "https://images.unsplash.com/photo-1506765515386-0a8e03639e4b?w=400",
        "type": "house", "department": "LA LIBERTAD", "transaction_type": "sale"
    },
    {
        "id": "77", "title": "Depa céntrico Trujillo", "price": 950, "bedrooms": 3, "bathrooms": 2, "area": 90,
        "district": "Trujillo", "latitude": -8.1150, "longitude": -79.0300,
        "imageUrl": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400",
        "type": "apartment", "department": "LA LIBERTAD", "transaction_type": "rent"
    },
    {
        "id": "78", "title": "Casa en Otuzco", "price": 700, "bedrooms": 2, "bathrooms": 1, "area": 100,
        "district": "Otuzco", "latitude": -7.9050, "longitude": -78.5680,
        "imageUrl": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400",
        "type": "house", "department": "LA LIBERTAD", "transaction_type": "rent"
    },

    # --- LAMBAYEQUE (5) ---
    {
        "id": "79", "title": "Depa en Chiclayo", "price": 800, "bedrooms": 2, "bathrooms": 1, "area": 65,
        "district": "Chiclayo", "latitude": -6.7710, "longitude": -79.8400,
        "imageUrl": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400",
        "type": "apartment", "department": "LAMBAYEQUE", "transaction_type": "rent"
    },
    {
        "id": "80", "title": "Casa de playa en Pimentel", "price": 1700, "bedrooms": 3, "bathrooms": 2, "area": 130,
        "district": "Pimentel", "latitude": -6.8370, "longitude": -79.9340,
        "imageUrl": "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=400",
        "type": "house", "department": "LAMBAYEQUE", "transaction_type": "rent"
    },
    {
        "id": "81", "title": "Terreno en Lambayeque", "price": 40000, "bedrooms": 0, "bathrooms": 0, "area": 300,
        "district": "Lambayeque", "latitude": -6.7050, "longitude": -79.9050,
        "imageUrl": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=400",
        "type": "house", "department": "LAMBAYEQUE", "transaction_type": "sale"
    },
    {
        "id": "82", "title": "Depa céntrico Chiclayo", "price": 900, "bedrooms": 3, "bathrooms": 2, "area": 85,
        "district": "Chiclayo", "latitude": -6.7730, "longitude": -79.8420,
        "imageUrl": "https://images.unsplash.com/photo-1505691938895-1758d7FEB511?w=400",
        "type": "apartment", "department": "LAMBAYEQUE", "transaction_type": "rent"
    },
    {
        "id": "83", "title": "Casa en Ferreñafe", "price": 750, "bedrooms": 2, "bathrooms": 1, "area": 90,
        "district": "Ferreñafe", "latitude": -6.6400, "longitude": -79.7900,
        "imageUrl": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=400",
        "type": "house", "department": "LAMBAYEQUE", "transaction_type": "rent"
    },

    # --- MADRE DE DIOS (5) ---
    {
        "id": "84", "title": "Casa en Puerto Maldonado", "price": 700, "bedrooms": 3, "bathrooms": 1, "area": 110,
        "district": "Tambopata", "latitude": -12.5930, "longitude": -69.1890,
        "imageUrl": "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=400",
        "type": "house", "department": "MADRE DE DIOS", "transaction_type": "rent"
    },
    {
        "id": "85", "title": "Depa céntrico", "price": 500, "bedrooms": 2, "bathrooms": 1, "area": 60,
        "district": "Tambopata", "latitude": -12.6000, "longitude": -69.1800,
        "imageUrl": "https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=400",
        "type": "apartment", "department": "MADRE DE DIOS", "transaction_type": "rent"
    },
    {
        "id": "86", "title": "Terreno en La Pampa", "price": 15000, "bedrooms": 0, "bathrooms": 0, "area": 500,
        "district": "Inambari", "latitude": -12.8500, "longitude": -69.6500,
        "imageUrl": "https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=400",
        "type": "house", "department": "MADRE DE DIOS", "transaction_type": "sale"
    },
    {
        "id": "87", "title": "Bungalow en selva", "price": 1000, "bedrooms": 1, "bathrooms": 1, "area": 50,
        "district": "Tambopata", "latitude": -12.6100, "longitude": -69.2000,
        "imageUrl": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400",
        "type": "house", "department": "MADRE DE DIOS", "transaction_type": "rent"
    },
    {
        "id": "88", "title": "Depa en Iberia", "price": 450, "bedrooms": 2, "bathrooms": 1, "area": 55,
        "district": "Iberia", "latitude": -11.4050, "longitude": -69.4900,
        "imageUrl": "https://images.unsplash.com/photo-1533779283484-8ad4940aa3a8?w=400",
        "type": "apartment", "department": "MADRE DE DIOS", "transaction_type": "rent"
    },

    # --- MOQUEGUA (5) ---
    {
        "id": "89", "title": "Depa en Moquegua", "price": 600, "bedrooms": 2, "bathrooms": 1, "area": 60,
        "district": "Moquegua", "latitude": -17.1980, "longitude": -70.9350,
        "imageUrl": "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=400",
        "type": "apartment", "department": "MOQUEGUA", "transaction_type": "rent"
    },
    {
        "id": "90", "title": "Casa en Ilo", "price": 900, "bedrooms": 3, "bathrooms": 2, "area": 120,
        "district": "Ilo", "latitude": -17.6450, "longitude": -71.3400,
        "imageUrl": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400",
        "type": "house", "department": "MOQUEGUA", "transaction_type": "rent"
    },
    {
        "id": "91", "title": "Terreno en Samegua", "price": 30000, "bedrooms": 0, "bathrooms": 0, "area": 300,
        "district": "Samegua", "latitude": -17.1900, "longitude": -70.9100,
        "imageUrl": "https://images.unsplash.com/photo-1506765515386-0a8e03639e4b?w=400",
        "type": "house", "department": "MOQUEGUA", "transaction_type": "sale"
    },
    {
        "id": "92", "title": "Depa céntrico Ilo", "price": 700, "bedrooms": 2, "bathrooms": 1, "area": 55,
        "district": "Ilo", "latitude": -17.6400, "longitude": -71.3450,
        "imageUrl": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400",
        "type": "apartment", "department": "MOQUEGUA", "transaction_type": "rent"
    },
    {
        "id": "93", "title": "Casa en Omate", "price": 500, "bedrooms": 2, "bathrooms": 1, "area": 90,
        "district": "Omate", "latitude": -16.6750, "longitude": -70.9700,
        "imageUrl": "https://images.unsplash.com/photo-1513584684374-8bab748fbf90?w=400",
        "type": "house", "department": "MOQUEGUA", "transaction_type": "rent"
    },

    # --- PASCO (5) ---
    {
        "id": "94", "title": "Casa en Cerro de Pasco", "price": 500, "bedrooms": 3, "bathrooms": 1, "area": 90,
        "district": "Chaupimarca", "latitude": -10.6840, "longitude": -76.2550,
        "imageUrl": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=400",
        "type": "house", "department": "PASCO", "transaction_type": "rent"
    },
    {
        "id": "95", "title": "Depa en Yanacancha", "price": 400, "bedrooms": 2, "bathrooms": 1, "area": 60,
        "district": "Yanacancha", "latitude": -10.6750, "longitude": -76.2500,
        "imageUrl": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
        "type": "apartment", "department": "PASCO", "transaction_type": "rent"
    },
    {
        "id": "96", "title": "Terreno en Oxapampa", "price": 70000, "bedrooms": 0, "bathrooms": 0, "area": 1000,
        "district": "Oxapampa", "latitude": -10.5780, "longitude": -75.4050,
        "imageUrl": "https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=400",
        "type": "house", "department": "PASCO", "transaction_type": "sale"
    },
    {
        "id": "97", "title": "Cabaña en Pozuzo", "price": 800, "bedrooms": 2, "bathrooms": 1, "area": 70,
        "district": "Pozuzo", "latitude": -10.0700, "longitude": -75.5500,
        "imageUrl": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400",
        "type": "house", "department": "PASCO", "transaction_type": "rent"
    },
    {
        "id": "98", "title": "Depa en Villa Rica", "price": 550, "bedrooms": 2, "bathrooms": 1, "area": 55,
        "district": "Villa Rica", "latitude": -10.7380, "longitude": -75.2700,
        "imageUrl": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400",
        "type": "apartment", "department": "PASCO", "transaction_type": "rent"
    },

    # --- PUNO (5) ---
    {
        "id": "102", "title": "Depa con vista al Titicaca", "price": 800, "bedrooms": 2, "bathrooms": 1, "area": 70,
        "district": "Puno", "latitude": -15.8420, "longitude": -70.0200,
        "imageUrl": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400",
        "type": "apartment", "department": "PUNO", "transaction_type": "rent"
    },
    {
        "id": "103", "title": "Casa en Juliaca", "price": 900, "bedrooms": 3, "bathrooms": 2, "area": 120,
        "district": "Juliaca", "latitude": -15.4950, "longitude": -70.1300,
        "imageUrl": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400",
        "type": "house", "department": "PUNO", "transaction_type": "rent"
    },
    {
        "id": "104", "title": "Terreno en Ayaviri", "price": 25000, "bedrooms": 0, "bathrooms": 0, "area": 300,
        "district": "Ayaviri", "latitude": -14.8800, "longitude": -70.5900,
        "imageUrl": "https://images.unsplash.com/photo-1506765515386-0a8e03639e4b?w=400",
        "type": "house", "department": "PUNO", "transaction_type": "sale"
    },
    {
        "id": "105", "title": "Depa céntrico Juliaca", "price": 600, "bedrooms": 2, "bathrooms": 1, "area": 60,
        "district": "Juliaca", "latitude": -15.4900, "longitude": -70.1350,
        "imageUrl": "https://images.unsplash.com/photo-1505691938895-1758d7FEB511?w=400",
        "type": "apartment", "department": "PUNO", "transaction_type": "rent"
    },
    {
        "id": "106", "title": "Casa en Ilave", "price": 500, "bedrooms": 2, "bathrooms": 1, "area": 80,
        "district": "Ilave", "latitude": -16.0800, "longitude": -69.6400,
        "imageUrl": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=400",
        "type": "house", "department": "PUNO", "transaction_type": "rent"
    },

    # --- SAN MARTIN (5) ---
    {
        "id": "107", "title": "Depa en Tarapoto", "price": 700, "bedrooms": 2, "bathrooms": 1, "area": 65,
        "district": "Tarapoto", "latitude": -6.4880, "longitude": -76.3680,
        "imageUrl": "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=400",
        "type": "apartment", "department": "SAN MARTIN", "transaction_type": "rent"
    },
    {
        "id": "108", "title": "Casa en Moyobamba", "price": 950, "bedrooms": 3, "bathrooms": 2, "area": 130,
        "district": "Moyobamba", "latitude": -6.0350, "longitude": -76.9700,
        "imageUrl": "https://images.unsplash.com/photo-1598228723793-52759bba239c?w=400",
        "type": "house", "department": "SAN MARTIN", "transaction_type": "rent"
    },
    {
        "id": "109", "title": "Terreno en Juanjui", "price": 35000, "bedrooms": 0, "bathrooms": 0, "area": 400,
        "district": "Juanjui", "latitude": -7.1780, "longitude": -76.7250,
        "imageUrl": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=400",
        "type": "house", "department": "SAN MARTIN", "transaction_type": "sale"
    },
    {
        "id": "110", "title": "Bungalow en Lamas", "price": 1100, "bedrooms": 1, "bathrooms": 1, "area": 50,
        "district": "Lamas", "latitude": -6.4180, "longitude": -76.5180,
        "imageUrl": "https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=400",
        "type": "house", "department": "SAN MARTIN", "transaction_type": "rent"
    },
    {
        "id": "111", "title": "Depa moderno Tarapoto", "price": 850, "bedrooms": 2, "bathrooms": 2, "area": 75,
        "district": "Tarapoto", "latitude": -6.4900, "longitude": -76.3700,
        "imageUrl": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400",
        "type": "apartment", "department": "SAN MARTIN", "transaction_type": "rent"
    },

    # --- TACNA (5) ---
    {
        "id": "112", "title": "Depa en Tacna", "price": 750, "bedrooms": 2, "bathrooms": 1, "area": 65,
        "district": "Tacna", "latitude": -18.0140, "longitude": -70.2530,
        "imageUrl": "https://images.unsplash.com/photo-1513584684374-8bab748fbf90?w=400",
        "type": "apartment", "department": "TACNA", "transaction_type": "rent"
    },
    {
        "id": "113", "title": "Casa céntrica Tacna", "price": 1000, "bedrooms": 3, "bathrooms": 2, "area": 120,
        "district": "Tacna", "latitude": -18.0100, "longitude": -70.2500,
        "imageUrl": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=400",
        "type": "house", "department": "TACNA", "transaction_type": "rent"
    },
    {
        "id": "114", "title": "Terreno en Locumba", "price": 20000, "bedrooms": 0, "bathrooms": 0, "area": 300,
        "district": "Locumba", "latitude": -17.6150, "longitude": -70.7600,
        "imageUrl": "https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=400",
        "type": "house", "department": "TACNA", "transaction_type": "sale"
    },
    {
        "id": "115", "title": "Depa amoblado Tacna", "price": 850, "bedrooms": 1, "bathrooms": 1, "area": 50,
        "district": "Tacna", "latitude": -18.0120, "longitude": -70.2550,
        "imageUrl": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
        "type": "apartment", "department": "TACNA", "transaction_type": "rent"
    },
    {
        "id": "116", "title": "Casa en Calana", "price": 900, "bedrooms": 2, "bathrooms": 1, "area": 100,
        "district": "Calana", "latitude": -17.9500, "longitude": -70.2000,
        "imageUrl": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400",
        "type": "house", "department": "TACNA", "transaction_type": "rent"
    },

    # --- TUMBES (5) ---
    {
        "id": "117", "title": "Casa de playa Zorritos", "price": 2000, "bedrooms": 3, "bathrooms": 2, "area": 150,
        "district": "Zorritos", "latitude": -3.6780, "longitude": -80.6800,
        "imageUrl": "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=400",
        "type": "house", "department": "TUMBES", "transaction_type": "rent"
    },
    {
        "id": "118", "title": "Depa en Tumbes", "price": 700, "bedrooms": 2, "bathrooms": 1, "area": 65,
        "district": "Tumbes", "latitude": -3.5660, "longitude": -80.4600,
        "imageUrl": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=400",
        "type": "apartment", "department": "TUMBES", "transaction_type": "rent"
    },
    {
        "id": "119", "title": "Terreno en Punta Sal", "price": 120000, "bedrooms": 0, "bathrooms": 0, "area": 500,
        "district": "Canoas de Punta Sal", "latitude": -4.0900, "longitude": -81.0200,
        "imageUrl": "https://images.unsplash.com/photo-1506765515386-0a8e03639e4b?w=400",
        "type": "house", "department": "TUMBES", "transaction_type": "sale"
    },
    {
        "id": "120", "title": "Depa céntrico Tumbes", "price": 800, "bedrooms": 3, "bathrooms": 1, "area": 80,
        "district": "Tumbes", "latitude": -3.5680, "longitude": -80.4550,
        "imageUrl": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400",
        "type": "apartment", "department": "TUMBES", "transaction_type": "rent"
    },
    {
        "id": "121", "title": "Casa en Zarumilla", "price": 900, "bedrooms": 3, "bathrooms": 2, "area": 110,
        "district": "Zarumilla", "latitude": -3.5050, "longitude": -80.2750,
        "imageUrl": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400",
        "type": "house", "department": "TUMBES", "transaction_type": "rent"
    },

    # --- UCAYALI (5) ---
    {
        "id": "122", "title": "Depa en Pucallpa", "price": 650, "bedrooms": 2, "bathrooms": 1, "area": 60,
        "district": "Calleria", "latitude": -8.3830, "longitude": -74.5300,
        "imageUrl": "https://images.unsplash.com/photo-1505691938895-1758d7FEB511?w=400",
        "type": "apartment", "department": "UCAYALI", "transaction_type": "rent"
    },
    {
        "id": "123", "title": "Casa en Yarinacocha", "price": 1000, "bedrooms": 3, "bathrooms": 2, "area": 130,
        "district": "Yarinacocha", "latitude": -8.3500, "longitude": -74.5500,
        "imageUrl": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=400",
        "type": "house", "department": "UCAYALI", "transaction_type": "rent"
    },
    {
        "id": "124", "title": "Terreno en Campo Verde", "price": 30000, "bedrooms": 0, "bathrooms": 0, "area": 500,
        "district": "Campo Verde", "latitude": -8.4800, "longitude": -74.7800,
        "imageUrl": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?w=400",
        "type": "house", "department": "UCAYALI", "transaction_type": "sale"
    },
    {
        "id": "125", "title": "Depa céntrico Pucallpa", "price": 750, "bedrooms": 2, "bathrooms": 1, "area": 70,
        "district": "Calleria", "latitude": -8.3800, "longitude": -74.5350,
        "imageUrl": "https://images.unsplash.com/photo-1523217582562-09d0def993a6?w=400",
        "type": "apartment", "department": "UCAYALI", "transaction_type": "rent"
    },
    {
        "id": "126", "title": "Casa en Aguaytia", "price": 800, "bedrooms": 2, "bathrooms": 1, "area": 90,
        "district": "Padre Abad", "latitude": -9.0380, "longitude": -75.5050,
        "imageUrl": "https://images.unsplash.com/photo-1598228723793-52759bba239c?w=400",
        "type": "house", "department": "UCAYALI", "transaction_type": "rent"
    }
]


# --- ¡FUNCIÓN get_properties() ACTUALIZADA! ---
# Ahora acepta filtros como parámetros query
@router.get("")
async def get_properties(
        district: Optional[str] = None,
        min_price: Optional[float] = Query(None, alias="min_price"),
        max_price: Optional[float] = Query(None, alias="max_price"),
        bedrooms: Optional[int] = None,
        property_type: Optional[str] = Query(None, alias="property_type"),
        transaction_type: Optional[str] = Query(None, alias="transaction_type")
):
    """Get all properties with optional filters"""

    # Empezamos con la lista completa
    filtered_properties = MOCK_PROPERTIES

    # Aplicamos cada filtro si está presente
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
        return {"error": "Property not found"}, 404
    return {"property": prop}