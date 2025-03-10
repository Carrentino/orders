from typing import Annotated

from fastapi import Depends

from src.integrations.cars import CarsClient
from src.integrations.notifications import NotificationsKafkaProducer
from src.services.order import OrderService
from src.web.depends.integrations import get_cars_client, get_notifications_kafka_producer
from src.web.depends.repository import get_order_repository
from src.repositories.order import OrderRepository


async def get_order_service(
    order_repository: Annotated[OrderRepository, Depends(get_order_repository)],
    cars_client: Annotated[CarsClient, Depends(get_cars_client)],
    notifications_kafka_producer: Annotated[NotificationsKafkaProducer, Depends(get_notifications_kafka_producer)],
) -> OrderService:
    return OrderService(
        order_repository=order_repository,
        cars_client=cars_client,
        notifications_kafka_producer=notifications_kafka_producer,
    )
