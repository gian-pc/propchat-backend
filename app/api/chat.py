from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatMessage(BaseModel):
    message: str

@router.post("")
async def chat(payload: ChatMessage):
    """Chat endpoint"""
    return {
        "response": f"Recibí tu mensaje: '{payload.message}'. Integración con Claude próximamente.",
        "properties": []
    }