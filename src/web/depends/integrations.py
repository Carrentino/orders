from src.integrations.cars import CarsClient
from src.integrations.notifications import NotificationsKafkaProducer
from src.integrations.users import UsersClient


async def get_cars_client() -> CarsClient:
    return CarsClient()


async def get_notifications_kafka_producer() -> NotificationsKafkaProducer:
    return NotificationsKafkaProducer()


async def get_users_client() -> UsersClient:
    return UsersClient()
