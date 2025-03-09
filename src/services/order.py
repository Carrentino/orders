from uuid import UUID

import httpx
from fastapi.params import Depends

from src.db.models.order import Order
from src.integrations.cars import CarsClient
from src.repositories.order import OrderRepository
from src.services.cars_cache import CarCacheService
from src.web.api.orders.schems import LessorOrdersQueryParams


class OrderService:
    def __init__(self, order_repository: OrderRepository, cars_client: CarsClient) -> None:
        self.order_repository = order_repository
        self.cars_client = cars_client

    async def _add_car_objects(self, orders_data) -> list[Order]:
        not_found_cars = []
        for order in orders_data['data']:
            order_car_id = order.car_id
            car_obj = await CarCacheService.get_car(order_car_id)
            if car_obj is None:
                not_found_cars.append(order_car_id)
            else:
                order.car = dict(car_obj)

        if not_found_cars:
            filters = {"car__id": not_found_cars}
            try:
                response = await self.cars_client.get_cars_with_filters(**filters)
                car_objs = response.json()['data']
            except httpx.HTTPStatusError:
                car_objs = [{'id': car_id} for car_id in not_found_cars]

            car_dict = {car['id']: car for car in car_objs}
            for order in orders_data['data']:
                if order.car_id in car_dict:
                    order.car = car_dict[order.car_id]

        return orders_data

    async def get_lessor_orders(self, user_id: UUID, params: LessorOrdersQueryParams = Depends()) -> list[Order]:
        filters = {"lessor_id": user_id}
        if params.car_id:
            filters["car_id"] = params.car_id
        if params.status:
            filters["status"] = params.status
        orders_data = await self.order_repository.get_paginated_sorted_list(
            limit=params.limit,
            offset=params.offset,
            sort_by=params.sort_by,
            sort_direction=params.sort_direction,
            **filters,
        )

        return await self._add_car_objects(orders_data)

    async def get_renter_orders(self, user_id: UUID, params: LessorOrdersQueryParams = Depends()) -> list[Order]:
        filters = {"renter_id": user_id}
        if params.car_id:
            filters["car_id"] = params.car_id
        if params.status:
            filters["status"] = params.status
        orders_data = await self.order_repository.get_paginated_sorted_list(
            limit=params.limit,
            offset=params.offset,
            sort_by=params.sort_by,
            sort_direction=params.sort_direction,
            **filters,
        )

        return await self._add_car_objects(orders_data)
