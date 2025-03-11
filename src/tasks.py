from src.celery import celery_app
from src.db.models.order import Order


@celery_app.task
def generate_contract(order: Order):  # noqa
    # TODO: доделать в рамках задачи на создание договора
    pass
