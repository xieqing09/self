from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from app.db.base import Base
import uuid

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    upload_id = Column(String(36), ForeignKey("uploads.id"))
    sender = Column(String(255))
    content = Column(Text)
    timestamp = Column(DateTime, nullable=True)
    role = Column(String(50), default="user") # user or assistant
    raw_data = Column(JSON, nullable=True)
    
    # upload = relationship("Upload", back_populates="messages")
