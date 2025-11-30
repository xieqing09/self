from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    model: str = "llama3.1:8b"
    history: list[dict] = []

class ChatResponse(BaseModel):
    response: str
