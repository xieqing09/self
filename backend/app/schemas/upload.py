from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UploadBase(BaseModel):
    filename: str

class UploadCreate(UploadBase):
    pass

class UploadResponse(UploadBase):
    id: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
