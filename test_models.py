import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Carga tu API Key del .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: No se encontró GEMINI_API_KEY en tu .env")
    exit()

print("Configurando con la API Key...")
genai.configure(api_key=api_key)

# 2. Le pedimos a Google la lista de modelos
print("Buscando modelos disponibles para tu API key...")
try:
    found_model = False
    for m in genai.list_models():
        # 3. Filtramos solo los modelos que saben "chatear" (generateContent)
        if 'generateContent' in m.supported_generation_methods:
            print(f"--- Modelo Encontrado ---")
            print(f"Nombre: {m.name}")
            print("--------------------------")
            found_model = True

    if not found_model:
        print("\n¡ERROR!")
        print("No se encontró ningún modelo que soporte 'generateContent'.")
        print("Esto casi siempre es un problema de permisos o de facturación en tu proyecto de Google Cloud.")
        print("Asegúrate de haber HABILITADO la API de Vertex AI y ASOCIADO la facturación.")

except Exception as e:
    print(f"\nError al conectar con Google: {e}")
    print("Asegúrate de que tu API Key sea 100% correcta.")