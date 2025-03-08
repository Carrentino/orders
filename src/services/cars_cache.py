import json
from uuid import UUID

from helpers.redis_client.client import RedisClient

from src.services.consts import CAR_CACHE_TTL
from src.settings import get_settings


class CarCacheService:
    @staticmethod
    async def get_car(car_id: UUID) -> dict | None:
        async with RedisClient(get_settings().redis.url) as rc:
            car_data = await rc.get(str(car_id))
            if car_data:
                return json.loads(car_data)
            return None

    @staticmethod
    async def set_car(car_id: UUID, car_data: dict) -> None:
        async with RedisClient(get_settings().redis.url) as rc:
            await rc.set(str(car_id), json.dumps(car_data), ex=CAR_CACHE_TTL)
