from uuid import UUID

from pydantic import BaseModel


class PushNotification(BaseModel):
    to_user_id: UUID
    title: str
    body: str
