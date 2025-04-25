from helpers.kafka.producer import KafkaProducer

from src.settings import get_settings
from src.integrations.schemas import PushNotification, EmailMsg


class NotificationsKafkaProducer(KafkaProducer):
    notifications_topic = get_settings().kafka.notifications_topic
    emails_topic = get_settings().kafka.emails_topic

    def __init__(self) -> None:
        super().__init__(str(get_settings().kafka.url))

    async def send_push_notification(self, push: PushNotification) -> None:
        await self.send_model_message(self.notifications_topic, push)

    async def send_email(self, email: EmailMsg) -> None:
        await self.send_model_message(self.emails_topic, email)
