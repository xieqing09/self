from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "WeChatFinetune"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str
    REDIS_URL: str
    
    # Storage Config
    USE_LOCAL_STORAGE: bool = False
    LOCAL_STORAGE_PATH: str = "./storage_data"
    
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_UPLOADS: str = "uploads"
    MINIO_BUCKET_MODELS: str = "models"
    MINIO_SECURE: bool = False
    
    # Celery Config
    CELERY_ALWAYS_EAGER: bool = False
    
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Model Config
    OLLAMA_BASE_MODEL: str = "llama3.1:8b"
    OLLAMA_API_URL: str = "http://localhost:11434/api"

    class Config:
        env_file = ".env"

settings = Settings()
