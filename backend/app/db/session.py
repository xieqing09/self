from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Handle SQLite specific connect args
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Async Engine
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True,
    connect_args=connect_args
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Sync Engine (for Celery)
# Convert async URL to sync URL (e.g. mysql+aiomysql -> mysql+pymysql)
SYNC_DATABASE_URL = settings.DATABASE_URL.replace("+aiomysql", "+pymysql").replace("+aiosqlite", "")
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=True,
    connect_args=connect_args if settings.DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
