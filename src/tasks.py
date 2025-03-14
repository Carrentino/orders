from uuid import UUID

from src.celery_conf import celery_app


@celery_app.task
def generate_contract(order_id: UUID):  # noqa
    # TODO: доделать в рамках задачи на создание договора
    pass
