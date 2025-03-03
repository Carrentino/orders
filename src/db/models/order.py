import uuid
from datetime import datetime
from enum import Enum

from aiokafka.protocol.types import Boolean
from sqlalchemy import String, Index, DateTime, ForeignKey
from helpers.sqlalchemy.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.consts import OrderStatus
from src.db.models.contract import Contract


class Order(Base):
    __tablename__ = 'orders'

    car_id: Mapped[uuid.UUID] = mapped_column(String)
    renter_id: Mapped[uuid.UUID] = mapped_column(String)
    lessor_id: Mapped[uuid.UUID] = mapped_column(String)
    chat_room_id: Mapped[uuid.UUID] = mapped_column(String)
    desired_start_datetime: Mapped[datetime] = mapped_column(DateTime)
    desired_finish_datetime: Mapped[datetime] = mapped_column(DateTime)
    start_rent_datetime: Mapped[datetime | None] = mapped_column(DateTime)
    finish_rent_datetime: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.UNDER_CONSIDERATION, nullable=False
    )
    is_renter_start_order: Mapped[bool] = mapped_column(Boolean, default=False)
    is_lessor_start_order: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey('contracts.id'), nullable=True)
    contract: Mapped[Contract] = relationship("Contract", back_populates="orders")

    __table_args__ = (
        Index('ix_orders_renter_id', 'renter_id', postgresql_using='btree'),
        Index('ix_orders_lessor_id', 'lessor_id', postgresql_using='btree'),
    )
