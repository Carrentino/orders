import uuid

import pytest
from helpers.jwt import encode_jwt
from httpx import AsyncClient
from starlette import status

from src.settings import get_settings
from src.web.api.orders.schems import LessorOrdersList
from tests.factories.order import OrderFactory


async def test_get_list_lessor_orders(client: AsyncClient) -> None:
    user_id = uuid.uuid4()
    orders = await OrderFactory.create_batch(3, lessor_id=user_id)
    payload = {'user_id': str(user_id), 'status': 'VERIFIED'}
    token = encode_jwt(get_settings().jwt_key.get_secret_value(), payload, algorithm="HS256")
    response = await client.get('/api/orders/lessor-orders/', headers={'X-Auth-Token': token})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 3
    assert response.json()['data'][0] == LessorOrdersList.model_validate(orders[0]).model_dump(mode='json')


@pytest.mark.parametrize(
    'filter,count', [('car_id=9e93b46a-853d-4110-85e2-b32e75eba2a1', 0), ('status=Отклонен', 0), ('', 3)]  # noqa
)
async def test_get_list_lessor_with_filters(filter, count, client: AsyncClient) -> None:
    user_id = uuid.uuid4()
    orders = await OrderFactory.create_batch(3, lessor_id=user_id)
    payload = {'user_id': str(user_id), 'status': 'VERIFIED'}
    token = encode_jwt(get_settings().jwt_key.get_secret_value(), payload, algorithm="HS256")
    response = await client.get(f'/api/orders/lessor-orders/?{filter}', headers={'X-Auth-Token': token})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == count
    if count != 0:
        assert response.json()['data'][0] == LessorOrdersList.model_validate(orders[0]).model_dump(mode='json')


async def test_get_list_lessor_pagination(client: AsyncClient) -> None:
    user_id = uuid.uuid4()
    await OrderFactory.create_batch(20, lessor_id=user_id)
    payload = {'user_id': str(user_id), 'status': 'VERIFIED'}
    token = encode_jwt(get_settings().jwt_key.get_secret_value(), payload, algorithm="HS256")
    response = await client.get('/api/orders/lessor-orders/', headers={'X-Auth-Token': token})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['data']) == 10
    assert response.json()['total'] == 20
    assert response.json()['total_pages'] == 2
