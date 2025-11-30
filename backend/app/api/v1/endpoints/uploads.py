from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.upload import UploadResponse
from app.models.upload import Upload
from app.models.message import Message
from app.schemas.message import MessageResponse
from app.utils.storage import storage
from app.core.config import settings
from app.workers.tasks import parse_upload
import uuid

router = APIRouter()

from sqlalchemy import select

@router.get("/", response_model=list[UploadResponse])
async def list_uploads(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Upload).offset(skip).limit(limit))
    uploads = result.scalars().all()
    return uploads

@router.post("/", response_model=UploadResponse)
async def upload_chat_history(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    file_content = await file.read()
    file_name = f"{uuid.uuid4()}-{file.filename}"
    
    try:
        path = storage.upload_file(file_content, file_name, settings.MINIO_BUCKET_UPLOADS)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    db_upload = Upload(
        filename=file.filename,
        storage_path=path,
        status="uploaded"
    )
    db.add(db_upload)
    await db.commit()
    await db.refresh(db_upload)

    # Trigger async parsing task
    parse_upload.delay(db_upload.id, path)

    return db_upload

@router.get("/{upload_id}", response_model=UploadResponse)
async def get_upload_status(upload_id: str, db: AsyncSession = Depends(get_db)):
    upload = await db.get(Upload, upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")
    return upload

@router.get("/{upload_id}/messages", response_model=list[MessageResponse])
async def get_upload_messages(
    upload_id: str, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    # Check if upload exists
    upload = await db.get(Upload, upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")
        
    # Fetch messages
    result = await db.execute(
        select(Message)
        .where(Message.upload_id == upload_id)
        .order_by(Message.timestamp)
        .limit(limit)
    )
    messages = result.scalars().all()
    return messages
