from typing import Annotated

from fastapi import Depends

from src.integrations.cars import CarsClient
from src.services.order import OrderService
from src.web.depends.integrations import get_cars_client
from src.web.depends.repository import get_order_repository
from src.repositories.order import OrderRepository


async def get_order_service(
    order_repository: Annotated[OrderRepository, Depends(get_order_repository)],
    cars_client: Annotated[CarsClient, Depends(get_cars_client)],
) -> OrderService:
    return OrderService(order_repository=order_repository, cars_client=cars_client)
