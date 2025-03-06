import math
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext

from src.services.order import OrderService
from src.web.api.orders.schems import (
    LessorOrderList,
    PaginatedLessorOrdersListResp,
    LessorOrdersQueryParams,
    PaginatedRenterOrderListResp,
    RenterOrderList,
)
from src.web.depends.service import get_order_service

orders_router = APIRouter()


@orders_router.get('/lessor-orders/', response_model=PaginatedLessorOrdersListResp)
async def lessor_orders(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)],
    query_params: LessorOrdersQueryParams = Depends(),
):
    filters = {}
    if query_params.car_id:
        filters['car_id'] = UUID(query_params.car_id)
    if query_params.status:
        filters['status'] = query_params.status

    orders = await order_service.get_lessor_orders(current_user.user_id, params=query_params)
    total_pages = math.ceil(orders['total'] / query_params.size)

    return PaginatedLessorOrdersListResp(
        page=orders['page'],
        size=orders['size'],
        total=orders['total'],
        total_pages=total_pages,
        data=[LessorOrderList.model_validate(order) for order in orders['data']],
    )


@orders_router.get('/renter-orders/', response_model=PaginatedRenterOrderListResp)
async def renter_orders(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)],
    query_params: LessorOrdersQueryParams = Depends(),
):
    filters = {}
    if query_params.car_id:
        filters['car_id'] = UUID(query_params.car_id)
    if query_params.status:
        filters['status'] = query_params.status

    orders = await order_service.get_renter_orders(current_user.user_id, params=query_params)
    total_pages = math.ceil(orders['total'] / query_params.size)

    return PaginatedRenterOrderListResp(
        page=orders['page'],
        size=orders['size'],
        total=orders['total'],
        total_pages=total_pages,
        data=[RenterOrderList.model_validate(order) for order in orders['data']],
    )
