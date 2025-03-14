from unittest.mock import patch, AsyncMock

from httpx import AsyncClient
from starlette import status

from src.db.consts import OrderStatus
from tests.factories.order import OrderFactory


@patch('src.integrations.notifications.NotificationsKafkaProducer.send_push_notification', new_callable=AsyncMock)
@patch('src.integrations.notifications.NotificationsKafkaProducer.__init__')
async def test_accept_order(mock_kafka_init, mock_send_push, auth_client: AsyncClient, session):
    mock_send_push.return_value = None
    mock_kafka_init.return_value = None
    order = await OrderFactory.create(lessor_id=auth_client.user_id)
    intersection_order = await OrderFactory.create(
        car_id=order.car_id,
        desired_start_datetime=order.desired_start_datetime,
        desired_finish_datetime=order.desired_finish_datetime,
    )
    response = await auth_client.patch(f'/api/orders/{order.id}/accept/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    await session.refresh(order)
    assert order.status == OrderStatus.ACCEPTED
    await session.refresh(intersection_order)
    assert intersection_order.status == OrderStatus.REJECTED


@patch('src.integrations.notifications.NotificationsKafkaProducer.send_push_notification', new_callable=AsyncMock)
@patch('src.integrations.notifications.NotificationsKafkaProducer.__init__')
async def test_reject_order(mock_kafka_init, mock_send_push, auth_client: AsyncClient, session):
    mock_send_push.return_value = None
    mock_kafka_init.return_value = None
    order = await OrderFactory.create(lessor_id=auth_client.user_id)
    response = await auth_client.patch(f'/api/orders/{order.id}/reject/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    await session.refresh(order)
    assert order.status == OrderStatus.REJECTED


@patch('src.integrations.notifications.NotificationsKafkaProducer.send_push_notification', new_callable=AsyncMock)
@patch('src.integrations.notifications.NotificationsKafkaProducer.__init__')
async def test_cancel_order(mock_kafka_init, mock_send_push, auth_client: AsyncClient, session):
    mock_send_push.return_value = None
    mock_kafka_init.return_value = None
    order = await OrderFactory.create(renter_id=auth_client.user_id)
    response = await auth_client.patch(f'/api/orders/{order.id}/cancel/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    await session.refresh(order)
    assert order.status == OrderStatus.CANCELED
