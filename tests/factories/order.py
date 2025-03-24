import uuid
from datetime import datetime, timedelta

import factory

from src.db.consts import OrderStatus
from src.db.models.order import Order
from tests.factories.base import BaseSqlAlchemyFactory


class OrderFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = Order

    car_id = factory.LazyFunction(uuid.uuid4)
    renter_id = factory.LazyFunction(uuid.uuid4)
    lessor_id = factory.LazyFunction(uuid.uuid4)
    chat_room_id = factory.LazyFunction(uuid.uuid4)
    desired_start_datetime = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(days=1))
    desired_finish_datetime = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(days=2))
    start_rent_datetime = factory.LazyFunction(lambda: None)
    finish_rent_datetime = factory.LazyFunction(lambda: None)
    status = OrderStatus.UNDER_CONSIDERATION
    total_price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
