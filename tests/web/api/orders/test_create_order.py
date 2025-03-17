import datetime
import uuid

import pytest
from asyncpg.pgproto.pgproto import timedelta
from httpx import AsyncClient, Response, Request
from sqlalchemy import text
from starlette import status
from unittest.mock import patch, AsyncMock


from src.db.consts import OrderStatus
from src.db.models.order import Order
from src.settings import get_settings
from src.web.api.orders.schems import CreateOrderReq
from tests.factories.order import OrderFactory


@patch('src.integrations.cars.CarsClient.get_cars_with_filters', new_callable=AsyncMock)
@patch('src.integrations.notifications.NotificationsKafkaProducer.send_push_notification', new_callable=AsyncMock)
@patch('src.integrations.notifications.NotificationsKafkaProducer.__init__')
async def test_create_order(
    mock_kafka_init: AsyncMock, mock_send_push: AsyncMock, mock_cars: AsyncMock, auth_client: AsyncClient, session
) -> None:
    lessor_id = uuid.uuid4()
    car_id = uuid.uuid4()
    mock_cars.return_value = Response(
        json={'data': [{'id': str(car_id), 'model': 'BMW', 'user_id': str(lessor_id), 'price': 500}]},
        status_code=status.HTTP_200_OK,
        request=Request(method='get', url=get_settings().base_cars_url.get_secret_value()),
    )
    mock_send_push.return_value = None
    mock_kafka_init.return_value = None
    desired_start_datetime = datetime.datetime.now()
    desired_finish_datetime = datetime.datetime.now() + timedelta(hours=1)
    data = CreateOrderReq(
        car_id=car_id,
        desired_start_datetime=desired_start_datetime,
        desired_finish_datetime=desired_finish_datetime,
    )
    response = await auth_client.post('/api/orders/', json=data.model_dump(mode='json'))
    assert response.status_code == status.HTTP_201_CREATED
    order_id = response.json().get('id')
    total_price = (desired_finish_datetime - desired_start_datetime).total_seconds() / 3600 * 500
    assert order_id is not None
    order = await session.get(Order, order_id)
    assert order.lessor_id == lessor_id
    assert order.car_id == car_id
    assert order.total_price == total_price


@pytest.mark.parametrize(  # noqa
    'desired_start_datetime,desired_finish_datetime',  # noqa
    [
        (datetime.datetime.now() + timedelta(minutes=50), datetime.datetime.now() + timedelta(hours=5)),
        (datetime.datetime.now() + timedelta(minutes=1), datetime.datetime.now() + timedelta(hours=2)),
        (datetime.datetime.now() - timedelta(hours=1), datetime.datetime.now() + timedelta(hours=1)),
    ],
)
@patch('src.integrations.cars.CarsClient.get_cars_with_filters', new_callable=AsyncMock)
@patch('src.integrations.notifications.NotificationsKafkaProducer.send_push_notification', new_callable=AsyncMock)
@patch('src.integrations.notifications.NotificationsKafkaProducer.__init__')
async def test_error_create_order_with_orders_with_accepted_status(
    mock_kafka_init: AsyncMock,
    mock_send_push: AsyncMock,
    mock_cars: AsyncMock,
    auth_client: AsyncClient,
    desired_start_datetime,
    desired_finish_datetime,
    session,
):
    await session.execute(text('TRUNCATE TABLE orders'))  # noqa
    await session.commit()
    lessor_id = uuid.uuid4()
    car_id = uuid.uuid4()
    await OrderFactory.create(
        desired_start_datetime=datetime.datetime.now(),
        desired_finish_datetime=datetime.datetime.now() + timedelta(hours=3),
        status=OrderStatus.ACCEPTED,
        car_id=car_id,
    )
    mock_cars.return_value = Response(
        json={'data': [{'id': str(car_id), 'model': 'BMW', 'user_id': str(lessor_id), 'price': 500}]},
        status_code=status.HTTP_200_OK,
        request=Request(method='get', url=get_settings().base_cars_url.get_secret_value()),
    )
    mock_send_push.return_value = None
    mock_kafka_init.return_value = None
    data = CreateOrderReq(
        car_id=car_id, desired_start_datetime=desired_start_datetime, desired_finish_datetime=desired_finish_datetime
    )
    response = await auth_client.post('/api/orders/', json=data.model_dump(mode='json'))

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(  # noqa
    'desired_start_datetime,desired_finish_datetime',  # noqa
    [
        (datetime.datetime.now() + timedelta(minutes=50), datetime.datetime.now() + timedelta(hours=5)),
        (datetime.datetime.now() + timedelta(minutes=1), datetime.datetime.now() + timedelta(hours=2)),
        (datetime.datetime.now() - timedelta(hours=1), datetime.datetime.now() + timedelta(hours=1)),
    ],
)
@patch('src.integrations.cars.CarsClient.get_cars_with_filters', new_callable=AsyncMock)
@patch('src.integrations.notifications.NotificationsKafkaProducer.send_push_notification', new_callable=AsyncMock)
@patch('src.integrations.notifications.NotificationsKafkaProducer.__init__')
async def test_create_order_with_orders_with_under_consideration_status(
    mock_kafka_init: AsyncMock,
    mock_send_push: AsyncMock,
    mock_cars: AsyncMock,
    auth_client: AsyncClient,
    desired_start_datetime,
    desired_finish_datetime,
    session,
):
    lessor_id = uuid.uuid4()
    car_id = uuid.uuid4()
    await session.execute(text('TRUNCATE TABLE orders'))
    await session.commit()
    await OrderFactory.create(
        desired_start_datetime=datetime.datetime.now(),
        desired_finish_datetime=datetime.datetime.now() + timedelta(hours=3),
        status=OrderStatus.UNDER_CONSIDERATION,
        car_id=car_id,
    )
    mock_cars.return_value = Response(
        json={'data': [{'id': str(car_id), 'model': 'BMW', 'user_id': str(lessor_id), 'price': 500}]},
        status_code=status.HTTP_200_OK,
        request=Request(method='get', url=get_settings().base_cars_url.get_secret_value()),
    )
    mock_send_push.return_value = None
    mock_kafka_init.return_value = None
    data = CreateOrderReq(
        car_id=car_id, desired_start_datetime=desired_start_datetime, desired_finish_datetime=desired_finish_datetime
    )
    response = await auth_client.post('/api/orders/', json=data.model_dump(mode='json'))

    assert response.status_code == status.HTTP_201_CREATED
