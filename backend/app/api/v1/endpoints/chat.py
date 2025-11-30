from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.config import settings
import httpx

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Build messages history
    # Ensure history format is correct (list of dicts with role and content)
    messages = request.history.copy() if request.history else []
    messages.append({"role": "user", "content": request.message})
    
    payload = {
        "model": request.model,
        "messages": messages,
        "stream": False
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.OLLAMA_API_URL}/chat",
                json=payload
            )
            
            if response.status_code != 200:
                # Fallback error handling or specific logic
                raise HTTPException(status_code=response.status_code, detail=f"Ollama Error: {response.text}")
                
            data = response.json()
            # Check if 'message' exists in response (Ollama chat API)
            if "message" in data and "content" in data["message"]:
                return {"response": data["message"]["content"]}
            else:
                raise HTTPException(status_code=500, detail="Invalid response format from Ollama")
            
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Could not connect to Ollama: {exc}")
