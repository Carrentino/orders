from typing import Annotated

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext

from src.services.order_service import OrderService
from src.web.api.orders.schems import LessorOrdersList
from src.web.depends.service import get_order_service

orders_router = APIRouter()


@orders_router.get('/lessor-orders/', response_model=list[LessorOrdersList])
async def lessor_orders(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)],
):

    orders = await order_service.get_lessor_orders(current_user.user_id)
    return [LessorOrdersList.model_validate(order) for order in orders]
