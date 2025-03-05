from typing import Annotated

from fastapi import Depends

from src.services.order import OrderService
from src.web.depends.repository import get_order_repository
from src.repositories.order import OrderRepository


async def get_order_service(
    order_repository: Annotated[OrderRepository, Depends(get_order_repository)]
) -> OrderService:
    return OrderService(order_repository=order_repository)
