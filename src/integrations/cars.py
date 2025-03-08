from typing import Any
from uuid import UUID
from urllib.parse import urljoin

import requests
from helpers.clients.http_client import BaseApiClient

from src.services.cars_cache import CarCacheService


class CarsClient(BaseApiClient):
    _base_url = 'https://carrentino.ru/cars/api/v1/'

    async def get_car(self, car_id: UUID) -> int:  # noqa

        return 0

    async def get_cars_with_filters(self, **filters: dict[str, Any]) -> requests.Response:
        params = {}
        for key, value in filters.items():
            if value is not None:
                if isinstance(value, list):
                    params[key] = ",".join(str(v) for v in value)
                else:
                    params[key] = value
        response = await self.get(urljoin(self._base_url, ''), params=params)
        for car in response.json()['data']:
            await CarCacheService.set_car(car['id'], car)
        return response
