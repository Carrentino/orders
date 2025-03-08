import pytest
from httpx import AsyncClient
from starlette import status
from unittest.mock import patch, AsyncMock

from src.web.api.orders.schems import LessorOrderList
from tests.factories.order import OrderFactory


@patch('src.services.cars_cache.CarCacheService.get_car', new_callable=AsyncMock)
async def test_get_list_lessor_orders(mock_cache: AsyncMock, auth_client: AsyncClient) -> None:
    orders = await OrderFactory.create_batch(3, lessor_id=auth_client.user_id)
    mock_cache.return_value = {'id': "bimbimbambam", 'model': 'BMW'}
    response = await auth_client.get('/api/orders/lessor-orders/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 3
    orders[0].car = {'id': "bimbimbambam", 'model': 'BMW'}
    assert response.json()['data'][0] == LessorOrderList.model_validate(orders[0]).model_dump(mode='json')


@pytest.mark.parametrize(
    'filter,count', [('car_id=9e93b46a-853d-4110-85e2-b32e75eba2a1', 0), ('status=Отклонен', 0), ('', 3)]  # noqa
)
@patch('src.services.cars_cache.CarCacheService.get_car', new_callable=AsyncMock)
async def test_get_list_lessor_with_filters(mock_cache: AsyncMock, filter, count, auth_client: AsyncClient) -> None:
    orders = await OrderFactory.create_batch(3, lessor_id=auth_client.user_id)
    mock_cache.return_value = {'id': "bimbimbambam", 'model': 'BMW'}
    response = await auth_client.get(f'/api/orders/lessor-orders/?{filter}')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == count
    if count != 0:
        orders[0].car = {'id': "bimbimbambam", 'model': 'BMW'}
        assert response.json()['data'][0] == LessorOrderList.model_validate(orders[0]).model_dump(mode='json')


@patch('src.services.cars_cache.CarCacheService.get_car', new_callable=AsyncMock)
async def test_get_list_lessor_pagination(mock_cache: AsyncMock, auth_client: AsyncClient) -> None:
    await OrderFactory.create_batch(20, lessor_id=auth_client.user_id)
    mock_cache.return_value = {'id': "bimbimbambam", 'model': 'BMW'}
    response = await auth_client.get('/api/orders/lessor-orders/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 20
    assert response.json()['total'] == 20
    assert response.json()['limit'] == 30
    assert response.json()['offset'] == 0
