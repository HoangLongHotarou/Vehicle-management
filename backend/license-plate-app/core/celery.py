# import time

# from celery import Celery

# from .config import settings

# celery = Celery(
#     'core',
#     broker=settings.REDIS_BROKER,
#     backend=settings.REDIS_BACKEND,
#     include=['api.tasks.worker']
# )