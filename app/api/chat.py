from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json  # <-- Asegúrate de que 'json' esté importado

# Cargamos las variables de entorno (el .env)
load_dotenv()

router = APIRouter(prefix="/api/chat", tags=["chat"])

# --- 1. Configurar el cliente de Gemini (Sin cambios) ---
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la API Key de Gemini.")

    genai.configure(api_key=api_key)
    generation_config = {"temperature": 0.7, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    # Usamos el modelo que SÍ está en tu lista
    model = genai.GenerativeModel(model_name="models/gemini-flash-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    print("Modelo de Gemini configurado exitosamente.")
except Exception as e:
    print(f"Error CRÍTICO al configurar Gemini: {e}")
    model = None


# --- 2. Definir los modelos de Pydantic (Sin cambios) ---
class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    response: str
    filters: Optional[Dict[str, Any]] = None


# --- 3. El Endpoint de Chat (MODIFICADO con el ARREGLO) ---
@router.post("", response_model=ChatResponse)
async def send_chat_message(request: ChatRequest):
    """
    Recibe un mensaje, extrae filtros con la IA y devuelve una respuesta + filtros.
    """
    if not model:
        raise HTTPException(status_code=500, detail="El modelo de IA no está configurado.")

    print(f"Recibido mensaje para IA: {request.message}")

    # Prompt mejorado con contexto peruano
    prompt = f"""
    Eres 'PropChat', un asistente de IA experto en bienes raíces en Perú.
    Tu tarea es analizar la consulta del usuario y devolver SIEMPRE un objeto JSON válido.
    El JSON debe tener dos claves: 'response' (tu respuesta amigable) y 'filters' (un objeto con los filtros extraídos).

    CONTEXTO PERUANO IMPORTANTE:
    - En Perú, "departamento" o "depa" = APARTMENT (tipo de vivienda)
    - Los departamentos/regiones geográficas son: LIMA, AREQUIPA, CUSCO, LORETO, PIURA, etc.
    - UTP = Universidad Tecnológica del Perú (tiene 5 campus en Lima)
    - Distritos populares Lima: Miraflores, San Isidro, Barranco, Surco, La Molina, San Miguel, Jesús María
    - Términos coloquiales: "depa" = apartment, "chamba" = trabajo, "cerca de mi u" = cerca de universidad

    CAMPUS UTP EN LIMA:
    - UTP Lima Centro (Cercado de Lima)
    - UTP Lima Norte (Los Olivos)
    - UTP San Juan de Lurigancho (SJL)
    - UTP Villa El Salvador (VES)
    - UTP Ate

    Los filtros válidos son:
    - "department": Un departamento/región de Perú: [AMAZONAS, ANCASH, APURIMAC, AREQUIPA, AYACUCHO, CAJAMARCA, CALLAO, CUSCO, HUANCAVELICA, HUANUCO, ICA, JUNIN, LA LIBERTAD, LAMBAYEQUE, LIMA, LORETO, MADRE DE DIOS, MOQUEGUA, PASCO, PIURA, PUNO, SAN MARTIN, TACNA, TUMBES, UCAYALI]
    - "district": Un distrito específico (ej: "Miraflores", "San Isidro", "Los Olivos")
    - "near": Lugar de referencia (ej: "UTP Lima Centro", "Parque Kennedy", "Mall del Sur")
    - "transaction_type": "rent" (alquiler) o "sale" (venta)
    - "property_type": "apartment" (departamento/depa) o "house" (casa)
    - "min_price": Un número
    - "max_price": Un número
    - "bedrooms": Un número (ej: 2 para "2 o más")

    Reglas:
    1. Si el usuario saluda (ej: "hola"), responde amablemente y pon 'filters' en null.
    2. Si menciona "departamento", "depa", "dpto" → property_type = "apartment"
    3. Si menciona "casa" → property_type = "house"
    4. Si dice "cerca de UTP" sin especificar → pregunta qué campus
    5. Si dice "UTP Lima Norte" o similar → near = "UTP Lima Norte", department = "LIMA"
    6. Si menciona distrito (Miraflores, San Isidro) SIN decir "cerca de" → district = "Miraflores", department = "LIMA"
    7. IMPORTANTE: Si usas el filtro "near", NO incluyas el filtro "district" (son incompatibles)
    8. Normaliza departamentos a MAYÚSCULAS sin acentos (ej: "Piura" -> "PIURA")
    9. Tu respuesta DEBE ser solo el JSON válido.

    Ejemplo 1:
    Usuario: "Hola, ¿qué tal?"
    Tu JSON:
    {{
      "response": "¡Hola! Soy PropChat, tu asistente de bienes raíces en Perú. ¿Qué tipo de propiedad buscas?",
      "filters": null
    }}

    Ejemplo 2:
    Usuario: "Busco depas en alquiler en Lima por menos de $1500"
    Tu JSON:
    {{
      "response": "¡Perfecto! Buscando departamentos en alquiler en Lima por menos de $1500.",
      "filters": {{
        "department": "LIMA",
        "transaction_type": "rent",
        "property_type": "apartment",
        "max_price": 1500
      }}
    }}

    Ejemplo 3:
    Usuario: "Quiero un depa cerca de UTP Lima Norte"
    Tu JSON:
    {{
      "response": "¡Entendido! Buscando departamentos cerca de UTP Lima Norte.",
      "filters": {{
        "department": "LIMA",
        "property_type": "apartment",
        "near": "UTP Lima Norte"
      }}
    }}

    Ejemplo 4:
    Usuario: "Casas en venta en Arequipa"
    Tu JSON:
    {{
      "response": "Buscando casas en venta en Arequipa.",
      "filters": {{
        "department": "AREQUIPA",
        "transaction_type": "sale",
        "property_type": "house"
      }}
    }}

    Ejemplo 5:
    Usuario: "Departamentos cerca de UTP"
    Tu JSON:
    {{
      "response": "¡Claro! UTP tiene varios campus en Lima. ¿A cuál te refieres? (Lima Centro, Lima Norte, SJL, VES, Ate)",
      "filters": null
    }}

    Usuario: "{request.message}"
    Tu JSON:
    """

    try:
        # 1. Generamos la respuesta de la IA
        ai_response = model.generate_content(prompt)
        ai_text = ai_response.text

        print(f"Respuesta de IA generada: {ai_text}")

        # --- ¡AQUÍ ESTÁ EL ARREGLO! ---
        # 2. Intentamos parsear el JSON
        try:
            # Limpiamos la respuesta
            json_text = ai_text.replace("```json\n", "").replace("\n```", "").strip()
            data = json.loads(json_text)

            # Si SÍ es JSON, lo devolvemos
            return ChatResponse(
                response=data.get("response", "Respuesta JSON inválida."),
                filters=data.get("filters", None)
            )

        except json.JSONDecodeError:
            # 3. Si NO es JSON, asumimos que es un saludo (como "hola")
            print(f"ADVERTENCIA: La IA no devolvió JSON. Devolviendo texto plano.")
            # Devolvemos el texto tal cual, sin filtros
            return ChatResponse(
                response=ai_text,
                filters=None
            )
        # --- FIN DEL ARREGLO ---

    except Exception as e:
        # 4. Si la API de Google falló (ej. por permisos o error de red)
        print(f"Error al generar respuesta de Gemini: {e}")
        raise HTTPException(status_code=500, detail="Error al procesar el mensaje con la IA.")