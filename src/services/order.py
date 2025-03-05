from uuid import UUID

from src.db.models.order import Order
from src.repositories.order import OrderRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    async def get_lessor_orders(
        self,
        user_id: UUID,
        page: int = 0,
        size: int = 10,
        sort_by: str = 'created_at',
        sort_direction: str = "asc",
        filters: dict | None = None,
    ) -> list[Order]:
        if filters is None:
            filters = {}
        filters['lessor_id'] = user_id
        return await self.order_repository.get_paginated_sorted_list(
            page=page,
            size=size,
            sort_by=sort_by,
            sort_direction=sort_direction,
            **filters,
        )
