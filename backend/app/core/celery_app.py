from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

if settings.CELERY_ALWAYS_EAGER:
    celery_app.conf.task_always_eager = True
    # Eager mode doesn't use Redis, so no broker connection issues

celery_app.conf.task_routes = {
    "app.workers.tasks.parse_upload": "main-queue",
    "app.workers.tasks.train_model": "training-queue",
}
