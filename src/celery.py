from celery import Celery

from .settings import get_settings

celery_app = Celery("orders", broker=get_settings().redis.url, backend=get_settings().redis.url)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
