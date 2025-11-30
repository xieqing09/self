from fastapi import APIRouter, HTTPException
from app.core.config import settings
import httpx

router = APIRouter()

@router.get("/")
async def list_models():
    """
    Proxy to Ollama /api/tags to list available models
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Ollama API: GET /api/tags
            response = await client.get(f"{settings.OLLAMA_API_URL}/tags")
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"Ollama Error: {response.text}")
                
            data = response.json()
            return data
            
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Could not connect to Ollama: {exc}")
