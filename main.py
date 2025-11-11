from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api import properties, chat

# --- ¡ESTA ES LA SOLUCIÓN! ---
# Comentamos esta línea. Estaba intentando conectarse a tu base de datos
# (que no estamos usando) y fallaba, "matando" la app antes de que Uvicorn la encontrara.
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/")
def read_root():
    return {
        "app": "PropChat API",
        "version": "v1",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include routers - ESTO ES LO IMPORTANTE
app.include_router(properties.router)
app.include_router(chat.router)