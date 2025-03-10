from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.db.consts import OrderStatus
from src.web.api.base_schems import BasePaginatedQueryParams, BasePaginatedResp
from src.web.api.orders.consts import OrderSortFields


class OrdersList(BaseModel):
    id: UUID
    car: dict
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


class PaginatedLessorOrdersListResp(BasePaginatedResp):
    data: list[OrdersList]


class BaseOrderQueryParams(BasePaginatedQueryParams):
    car_id: str | None = Field(None, description="Фильтр по uid авто")
    status: OrderStatus | None = Field(None, description="Фильтр по статусу")
    sort_by: OrderSortFields = Field(OrderSortFields.CREATED_AT, description="Поле для сортировки")
    sort_direction: str = Field("asc", pattern="^(asc|desc)$", description="Направление сортировки")


class LessorOrdersQueryParams(BaseOrderQueryParams):
    pass


class RenterOrdersQueryParams(BaseOrderQueryParams):
    pass


class PaginatedRenterOrderListResp(BasePaginatedResp):
    data: list[OrdersList]


class RenterOrderList(OrdersList):
    pass


class LessorOrderList(OrdersList):
    pass


class CreateOrderReq(BaseModel):
    car_id: UUID
    desired_start_datetime: datetime
    desired_finish_datetime: datetime
