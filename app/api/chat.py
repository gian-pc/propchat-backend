from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

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
        # ... (tus otros safety_settings) ...
    ]
    model = genai.GenerativeModel(model_name="models/gemini-flash-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    print("Modelo de Gemini configurado exitosamente.")
except Exception as e:
    print(f"Error CRÍTICO al configurar Gemini: {e}")
    model = None


# --- 2. Definir los modelos de Pydantic (MODIFICADOS) ---

class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None


# ¡NUEVA RESPUESTA! Ahora incluye 'filters'
class ChatResponse(BaseModel):
    response: str
    filters: Optional[Dict[str, Any]] = None  # Aquí irán los filtros (ej: {"department": "LIMA"})


# --- 3. El Endpoint de Chat (MODIFICADO) ---

# Esta es la lista de departamentos que tu mapa conoce.
# La IA usará esta lista para normalizar la entrada del usuario.
DEPARTAMENTOS_PERU = [
    "AMAZONAS", "ANCASH", "APURIMAC", "AREQUIPA", "AYACUCHO", "CAJAMARCA",
    "CALLAO", "CUSCO", "HUANCAVELICA", "HUANUCO", "ICA", "JUNIN",
    "LA LIBERTAD", "LAMBAYEQUE", "LIMA", "LORETO", "MADRE DE DIOS",
    "MOQUEGUA", "PASCO", "PIURA", "PUNO", "SAN MARTIN", "TACNA", "TUMBES", "UCAYALI"
]


@router.post("", response_model=ChatResponse)
async def send_chat_message(request: ChatRequest):
    """
    Recibe un mensaje, extrae filtros con la IA y devuelve una respuesta + filtros.
    """
    if not model:
        raise HTTPException(status_code=500, detail="El modelo de IA no está configurado.")

    print(f"Recibido mensaje para IA: {request.message}")

    # --- ¡NUEVO PROMPT AVANZADO! ---
    # Le pedimos a la IA que actúe como un extractor de JSON
    prompt = f"""
    Eres 'PropChat', un asistente de IA experto en bienes raíces en Perú.
    Tu tarea es analizar la consulta del usuario y devolver SIEMPRE un objeto JSON válido.
    El JSON debe tener dos claves: 'response' (tu respuesta amigable) y 'filters' (un objeto con los filtros extraídos).

    Los filtros válidos son:
    - "department": Un departamento de esta lista: {DEPARTAMENTOS_PERU}
    - "transaction_type": "rent" (alquiler) o "sale" (venta).
    - "property_type": "apartment" (departamento) o "house" (casa).
    - "min_price": Un número.
    - "max_price": Un número.
    - "bedrooms": Un número (ej: 2 para "2 o más").

    Reglas:
    1. Si el usuario saluda (ej: "hola"), responde amablemente y pon 'filters' en null.
    2. Si el usuario pide algo (ej: "Busco depas en Lima"), extrae los filtros.
    3. Si el usuario pide algo que no está en la lista (ej: "casas en Arequipa y Cusco"), escoge solo el PRIMERO ("AREQUIPA").
    4. Normaliza los departamentos a MAYÚSCULAS y sin acentos (ej: "Huánuco" -> "HUANUCO").
    5. Tu respuesta DEBE ser solo el JSON.

    Ejemplo 1:
    Usuario: "Hola, ¿qué tal?"
    Tu JSON:
    {{
      "response": "¡Hola! Soy PropChat, tu asistente de bienes raíces. ¿Qué buscas hoy?",
      "filters": null
    }}

    Ejemplo 2:
    Usuario: "Busco departamentos en alquiler en Lima por menos de $1500"
    Tu JSON:
    {{
      "response": "¡Entendido! Buscando departamentos en alquiler en Lima por menos de $1500. Te muestro los resultados.",
      "filters": {{
        "department": "LIMA",
        "transaction_type": "rent",
        "property_type": "apartment",
        "max_price": 1500
      }}
    }}

    Ejemplo 3:
    Usuario: "Quiero comprar una casa en Arequipa con 3 cuartos"
    Tu JSON:
    {{
      "response": "¡Perfecto! Buscando casas en venta en Arequipa con 3 o más dormitorios.",
      "filters": {{
        "department": "AREQUIPA",
        "transaction_type": "sale",
        "property_type": "house",
        "bedrooms": 3
      }}
    }}

    Usuario: "{request.message}"
    Tu JSON:
    """

    try:
        # Generamos la respuesta de la IA (que debería ser un string JSON)
        ai_response = model.generate_content(prompt)

        # Limpiamos la respuesta (a veces la IA añade ```json ... ```)
        json_text = ai_response.text.replace("```json\n", "").replace("\n```", "").strip()

        print(f"Respuesta JSON de IA generada: {json_text}")

        # Convertimos el string JSON en un objeto Python
        data = json.loads(json_text)

        # Devolvemos los datos parseados
        return ChatResponse(
            response=data.get("response", "No pude procesar eso."),
            filters=data.get("filters", None)
        )

    except Exception as e:
        print(f"Error al generar o parsear respuesta de Gemini: {e}")
        # Si la IA falla o el JSON es inválido, mandamos un error amigable
        return ChatResponse(
            response="Lo siento, tuve problemas para entender eso. ¿Puedes intentarlo de otra forma?",
            filters=None
        )