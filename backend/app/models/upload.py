from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid
import datetime
import enum

class UploadStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    FAILED = "failed"

class Upload(Base):
    __tablename__ = "uploads"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    filename = Column(String(255))
    storage_path = Column(String(255))
    status = Column(String(50), default=UploadStatus.UPLOADED)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # messages = relationship("Message", back_populates="upload")
