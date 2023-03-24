from celery import Celery
from .config import settings

celery = Celery(
    'core',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['api.tasks.worker']
)