from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    sender: str
    content: str
    role: str

class MessageResponse(MessageBase):
    id: str
    timestamp: Optional[datetime]
    
    class Config:
        from_attributes = True
