from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.db.consts import OrderStatus


class LessorOrdersList(BaseModel):
    id: UUID
    car_id: UUID
    renter_id: UUID
    lessor_id: UUID
    chat_room_id: UUID
    desired_start_datetime: datetime
    desired_finish_datetime: datetime
    start_rent_datetime: datetime | None = None
    finish_rent_datetime: datetime | None = None
    status: OrderStatus
    is_renter_start_order: bool
    is_lessor_start_order: bool
    contract_id: UUID | None = None

    class Config:
        from_attributes = True
