from src.integrations.cars import CarsClient
from src.integrations.notifications import NotificationsKafkaProducer


async def get_cars_client() -> CarsClient:
    return CarsClient()


async def get_notifications_kafka_producer() -> NotificationsKafkaProducer:
    return NotificationsKafkaProducer()
