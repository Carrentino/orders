import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Index, DateTime, ForeignKey, Boolean, Enum
from helpers.sqlalchemy.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.consts import OrderStatus


if TYPE_CHECKING:
    from src.db.models.contract import Contract


class Order(Base):
    __tablename__ = 'orders'

    car_id: Mapped[uuid.UUID]
    renter_id: Mapped[uuid.UUID]
    lessor_id: Mapped[uuid.UUID]
    chat_room_id: Mapped[uuid.UUID]
    desired_start_datetime: Mapped[datetime]
    desired_finish_datetime: Mapped[datetime]
    start_rent_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    finish_rent_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.UNDER_CONSIDERATION, nullable=False
    )
    is_renter_start_order: Mapped[bool] = mapped_column(Boolean, default=False)
    is_lessor_start_order: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('contracts.id'), nullable=True)
    contract: Mapped['Contract'] = relationship("Contract", back_populates="order")
    total_price: Mapped[Decimal]

    __table_args__ = (
        Index('ix_orders_renter_id', 'renter_id', postgresql_using='btree'),
        Index('ix_orders_lessor_id', 'lessor_id', postgresql_using='btree'),
    )
