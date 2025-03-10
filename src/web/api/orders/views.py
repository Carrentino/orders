from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext
from starlette import status

from src.errors.http import (
    AlreadyAcceptedOrdersForThisPeriodHttpError,
    CarsServiceHttpError,
    OrderRentPeriodDegreeOneHourHttpError,
    NotLessorOrderHttpError,
    OrderStatusMustBeUnderConsiderationHttpError,
    OrderNotFoundHttpError,
)
from src.errors.service import (
    AlreadyAcceptedOrdersForThisPeriodError,
    CarsServiceError,
    OrderRentPeriodDegreeOneHourError,
    OrderStatusMustBeUnderConsiderationError,
    NotLessorOrderError,
    OrderNotFoundError,
)
from src.services.order import OrderService
from src.web.api.base_schems import BaseCreateObjResp
from src.web.api.orders.schems import (
    LessorOrderList,
    PaginatedLessorOrdersListResp,
    LessorOrdersQueryParams,
    PaginatedRenterOrderListResp,
    RenterOrderList,
    CreateOrderReq,
)
from src.web.depends.service import get_order_service

orders_router = APIRouter()


@orders_router.get('/lessor-orders/', response_model=PaginatedLessorOrdersListResp)
async def lessor_orders(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)],
    query_params: LessorOrdersQueryParams = Depends(),
):
    orders = await order_service.get_lessor_orders(current_user.user_id, params=query_params)

    return PaginatedLessorOrdersListResp(
        limit=orders['limit'],
        offset=orders['offset'],
        total=orders['total'],
        data=[LessorOrderList.model_validate(order) for order in orders['data']],
    )


@orders_router.get('/renter-orders/', response_model=PaginatedRenterOrderListResp)
async def renter_orders(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)],
    query_params: LessorOrdersQueryParams = Depends(),
):
    orders = await order_service.get_renter_orders(current_user.user_id, params=query_params)
    return PaginatedRenterOrderListResp(
        limit=orders['limit'],
        offset=orders['offset'],
        total=orders['total'],
        data=[RenterOrderList.model_validate(order) for order in orders['data']],
    )


@orders_router.post('/', response_model=BaseCreateObjResp, status_code=status.HTTP_201_CREATED)
async def create_order(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)],
    req_data: CreateOrderReq,
) -> BaseCreateObjResp:
    try:
        order_id = await order_service.create_order(req_data, user_id=UUID(current_user.user_id))
        return BaseCreateObjResp(id=order_id)
    except AlreadyAcceptedOrdersForThisPeriodError:
        raise AlreadyAcceptedOrdersForThisPeriodHttpError from None
    except CarsServiceError:
        raise CarsServiceHttpError from None
    except OrderRentPeriodDegreeOneHourError:
        raise OrderRentPeriodDegreeOneHourHttpError from None


@orders_router.post('/{order_id}/accept/', status_code=status.HTTP_204_NO_CONTENT)
async def accept_order(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(get_order_service)],
    order_id: UUID,
):
    try:
        await order_service.accept_order(order_id=order_id, user_id=UUID(current_user.user_id))
    except NotLessorOrderError:
        raise NotLessorOrderHttpError from None
    except OrderStatusMustBeUnderConsiderationError:
        raise OrderStatusMustBeUnderConsiderationHttpError from None
    except OrderNotFoundError:
        raise OrderNotFoundHttpError from None
