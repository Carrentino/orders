from uuid import UUID

from fastapi.params import Depends

from src.db.models.order import Order
from src.repositories.order import OrderRepository
from src.web.api.orders.schems import LessorOrdersQueryParams


class OrderService:
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    async def get_lessor_orders(self, user_id: UUID, params: LessorOrdersQueryParams = Depends()) -> list[Order]:
        filters = {"lessor_id": user_id}
        if params.car_id:
            filters["car_id"] = params.car_id
        if params.status:
            filters["status"] = params.status
        return await self.order_repository.get_paginated_sorted_list(
            page=params.page,
            size=params.size,
            sort_by=params.sort_by,
            sort_direction=params.sort_direction,
            **filters,
        )
