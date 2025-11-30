from pydantic import BaseModel
from typing import Optional

class TrainingConfig(BaseModel):
    model: str = "llama3.1:8b"
    epochs: int = 3
    batchSize: int = 4
    learningRate: str = "2e-4"
    loraRank: int = 8

class TrainingRequest(BaseModel):
    dataset_id: str
    config: TrainingConfig

class TrainingResponse(BaseModel):
    task_id: str
    status: str
