from helpers.kafka.producer import KafkaProducer

from src.settings import get_settings
from src.integrations.schemas import PushNotification


class NotificationsKafkaProducer(KafkaProducer):
    notifications_topic = get_settings().notifications_topic

    def __init__(self) -> None:
        super().__init__(str(get_settings().notifications_kafka_url))

    async def send_push_notification(self, push: PushNotification) -> None:
        await self.send_model_message(self.notifications_topic, push)
