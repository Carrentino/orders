import math
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext

from src.db.consts import OrderStatus
from src.services.order import OrderService
from src.web.api.orders.consts import OrderSortFields
from src.web.api.orders.schems import LessorOrdersList, PaginatedLessorOrdersList
from src.web.depends.service import get_order_service

orders_router = APIRouter()


@orders_router.get('/lessor-orders/', response_model=PaginatedLessorOrdersList)
async def lessor_orders(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)],
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=10, default=10),
    car_id: str = Query(None, description='фильтр по uid авто'),
    status: OrderStatus = Query(None, description='фильтр по статусу'),
    sort_by: OrderSortFields = Query(OrderSortFields.CREATED_AT, description="Поле для сортировки"),
    sort_direction: str = Query("asc", regex="^(asc|desc)$", description="Направление сортировки"),
):
    filters = {}
    if car_id:
        filters['car_id'] = UUID(car_id)
    if status:
        filters['status'] = status

    orders = await order_service.get_lessor_orders(
        current_user.user_id, page=page, size=size, filters=filters, sort_by=sort_by, sort_direction=sort_direction
    )
    total_pages = math.ceil(orders['total'] / size)

    return {
        'page': orders['page'],
        'size': orders['size'],
        'total': orders['total'],
        'total_pages': total_pages,
        'data': [LessorOrdersList.model_validate(order) for order in orders['data']],
    }
