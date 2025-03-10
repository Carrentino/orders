from httpx import AsyncClient
from starlette import status

from src.db.consts import OrderStatus
from tests.factories.order import OrderFactory


async def test_accept_order(auth_client: AsyncClient, session):
    order = await OrderFactory.create(lessor_id=auth_client.user_id)
    response = await auth_client.post(f'/api/orders/{order.id}/accept/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    await session.refresh(order)
    assert order.status == OrderStatus.ACCEPTED
