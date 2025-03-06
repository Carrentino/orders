import pytest
from httpx import AsyncClient
from starlette import status

from src.web.api.orders.schems import RenterOrderList
from tests.factories.order import OrderFactory


async def test_get_list_renter_orders(auth_client: AsyncClient) -> None:
    orders = await OrderFactory.create_batch(3, renter_id=auth_client.user_id)
    response = await auth_client.get('/api/orders/renter-orders/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 3
    assert response.json()['data'][0] == RenterOrderList.model_validate(orders[0]).model_dump(mode='json')


@pytest.mark.parametrize(
    'filter,count', [('car_id=9e93b46a-853d-4110-85e2-b32e75eba2a1', 0), ('status=Отклонен', 0), ('', 3)]  # noqa
)
async def test_get_list_renter_with_filters(filter, count, auth_client: AsyncClient) -> None:
    orders = await OrderFactory.create_batch(3, renter_id=auth_client.user_id)
    response = await auth_client.get(f'/api/orders/renter-orders/?{filter}')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == count
    if count != 0:
        assert response.json()['data'][0] == RenterOrderList.model_validate(orders[0]).model_dump(mode='json')


async def test_get_list_renter_pagination(auth_client: AsyncClient) -> None:
    await OrderFactory.create_batch(20, renter_id=auth_client.user_id)
    response = await auth_client.get('/api/orders/renter-orders/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 10
    assert response.json()['total'] == 20
    assert response.json()['total_pages'] == 2
