import uuid
from unittest.mock import patch, AsyncMock

from httpx import Response

from src.integrations.cars import CarsClient
from src.services.cars_cache import CarCacheService


@patch('helpers.clients.http_client.BaseApiClient.get', new_callable=AsyncMock)
async def test_car_cache(mock: AsyncMock):
    car_id = uuid.uuid4()
    car = {'id': str(car_id), 'model': 'BMW'}
    mock.return_value = Response(status_code=200, json={'data': [car]})
    await CarsClient().get_cars_with_filters()
    car_from_cache = await CarCacheService.get_car(car_id)
    assert car_from_cache == car
