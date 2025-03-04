from uuid import UUID

from src.db.models.order import Order
from src.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    async def get_lessor_orders(self, user_id: UUID) -> list[Order]:
        return await self.order_repository.get_list(lessor_id=user_id)
