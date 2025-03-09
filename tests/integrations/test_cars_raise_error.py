from unittest.mock import patch, AsyncMock

import httpx
from httpx import AsyncClient, Response
from starlette import status

from src.integrations.cars import CarsClient
from tests.factories.order import OrderFactory


@patch('helpers.clients.http_client.BaseApiClient.get', new_callable=AsyncMock)
@patch('src.services.cars_cache.CarCacheService.get_car', new_callable=AsyncMock)
async def test_get_error_from_cars(mock_cache: AsyncMock, mock_cars: AsyncMock, auth_client: AsyncClient) -> None:
    orders = await OrderFactory.create_batch(1, lessor_id=auth_client.user_id)
    mock_cars.return_value = Response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, request=httpx.Request(method='get', url=CarsClient._base_url)
    )
    mock_cache.return_value = None
    response = await auth_client.get('/api/orders/lessor-orders/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['car'] == {'id': str(orders[0].car_id)}
    assert response.json()['total'] == 1
    assert response.json()['limit'] == 30
    assert response.json()['offset'] == 0
