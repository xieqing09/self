from fastapi import APIRouter, HTTPException, Depends
from app.schemas.training import TrainingRequest, TrainingResponse
from app.workers.tasks import train_model
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.upload import Upload

router = APIRouter()

@router.post("/", response_model=TrainingResponse)
async def start_training(
    request: TrainingRequest,
    db: AsyncSession = Depends(get_db)
):
    # Verify dataset exists
    upload = await db.get(Upload, request.dataset_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    if upload.status != "parsed":
        raise HTTPException(status_code=400, detail="Dataset must be parsed before training")

    # Trigger Celery task
    task = train_model.delay(request.dataset_id, request.config.dict())
    
    return {
        "task_id": task.id,
        "status": "started"
    }
