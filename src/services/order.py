import uuid
from uuid import UUID

import httpx
from asyncpg.pgproto.pgproto import timedelta
from fastapi.params import Depends

from src.db.consts import OrderStatus
from src.db.models.order import Order
from src.errors.service import (
    AlreadyAcceptedOrdersForThisPeriodError,
    CarsServiceError,
    OrderRentPeriodDegreeOneHourError,
    NotLessorOrderError,
    OrderStatusMustBeUnderConsiderationError,
    OrderNotFoundError,
    NotRenterOrderError,
)
from src.integrations.cars import CarsClient
from src.integrations.notifications import NotificationsKafkaProducer
from src.integrations.schemas import PushNotification
from src.repositories.order import OrderRepository
from src.services.cars_cache import CarCacheService
from src.web.api.orders.schems import LessorOrdersQueryParams, CreateOrderReq


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        cars_client: CarsClient,
        notifications_kafka_producer: NotificationsKafkaProducer,
    ) -> None:
        self.order_repository = order_repository
        self.cars_client = cars_client
        self.notifications_kafka_producer = notifications_kafka_producer

    async def _add_car_objects(self, orders_data, is_without_cache: bool) -> list[Order]:  # noqa
        not_found_cars = []
        if is_without_cache:
            not_found_cars = [order.car_id for order in orders_data['data']]
        else:
            for order in orders_data['data']:
                order_car_id = order.car_id
                car_obj = await CarCacheService.get_car(order_car_id)
                if car_obj is None:
                    not_found_cars.append(order_car_id)
                else:
                    order.car = dict(car_obj)

        if not_found_cars:
            filters = {"car__id": not_found_cars}
            try:
                response = await self.cars_client.get_cars_with_filters(**filters)
                car_objs = response.json()['data']
            except httpx.HTTPStatusError:
                car_objs = [{'id': str(car_id)} for car_id in not_found_cars]

            car_dict = {car['id']: car for car in car_objs}
            for order in orders_data['data']:
                if str(order.car_id) in car_dict:
                    order.car = car_dict[str(order.car_id)]

        return orders_data

    async def get_lessor_orders(self, user_id: UUID, params: LessorOrdersQueryParams = Depends()) -> list[Order]:
        filters = {"lessor_id": user_id}
        if params.car_id:
            filters["car_id"] = params.car_id
        if params.status:
            filters["status"] = params.status
        orders_data = await self.order_repository.get_paginated_sorted_list(
            limit=params.limit,
            offset=params.offset,
            sort_by=params.sort_by,
            sort_direction=params.sort_direction,
            **filters,
        )

        return await self._add_car_objects(orders_data, is_without_cache=False)

    async def get_renter_orders(self, user_id: UUID, params: LessorOrdersQueryParams = Depends()) -> list[Order]:
        filters = {"renter_id": user_id}
        if params.car_id:
            filters["car_id"] = params.car_id
        if params.status:
            filters["status"] = params.status
        orders_data = await self.order_repository.get_paginated_sorted_list(
            limit=params.limit,
            offset=params.offset,
            sort_by=params.sort_by,
            sort_direction=params.sort_direction,
            **filters,
        )

        return await self._add_car_objects(orders_data, is_without_cache=False)

    async def create_order(self, order_data: CreateOrderReq, user_id: UUID) -> UUID:
        intersection_orders = await self.order_repository.intersection_orders_with_target_status(
            order_data.desired_start_datetime,
            order_data.desired_finish_datetime,
            order_data.car_id,
            OrderStatus.ACCEPTED,
        )
        if order_data.desired_finish_datetime - timedelta(hours=1) < order_data.desired_start_datetime:
            raise OrderRentPeriodDegreeOneHourError from None
        if len(intersection_orders) > 0:
            raise AlreadyAcceptedOrdersForThisPeriodError from None
        new_order = Order(car_id=order_data.car_id)
        car_data = await self._add_car_objects({'data': [new_order]}, is_without_cache=True)
        car_info = car_data['data'][0].car
        lessor_id = car_info.get('user_id', None)
        if not lessor_id:
            raise CarsServiceError from None
        total_price = (
            (order_data.desired_finish_datetime - order_data.desired_start_datetime).total_seconds()
            / 3600
            * car_info.get('price')
        )
        order = Order(
            **dict(order_data),
            lessor_id=lessor_id,
            renter_id=user_id,
            chat_room_id=uuid.uuid4(),
            total_price=total_price,
        )
        # TODO: добавить интеграцию с чатом
        push = PushNotification(
            to_user_id=lessor_id,
            title='На ваш автомобиль оформили заявку!',
            body='На ваш авто только что оформили новую заявку! \n Поспеши договориться',
        )
        await self.notifications_kafka_producer.send_push_notification(push)
        return await self.order_repository.create(order)

    async def accept_order(self, order_id: UUID, user_id: UUID):
        from src.tasks import generate_contract

        order = await self.order_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError
        if order.lessor_id != user_id:
            raise NotLessorOrderError
        if order.status != OrderStatus.UNDER_CONSIDERATION:
            raise OrderStatusMustBeUnderConsiderationError
        intersection_orders = await self.order_repository.intersection_orders_with_target_status(
            order.desired_start_datetime, order.desired_finish_datetime, order.car_id, OrderStatus.UNDER_CONSIDERATION
        )
        for order in intersection_orders:
            await self.order_repository.update(order.id, status=OrderStatus.REJECTED)
            push = PushNotification(
                to_user_id=order.renter_id,
                title='К сожалению, вашу заявку на аренду отклонили(',
                body='Вашу заявку на аренду автомобиля отклонили \n Не отчаивайтесь и подберите новый вариант :)',
            )
            await self.notifications_kafka_producer.send_push_notification(push)

        push = PushNotification(
            to_user_id=order.renter_id,
            title='Поздравляем, вашу заявку на аренду одобрили',
            body='Поздравляем, вашу заявку на аренду одобрили \n Скорее обсуждать детали в чате',
        )
        await self.notifications_kafka_producer.send_push_notification(push)

        await self.order_repository.update(order_id, status=OrderStatus.ACCEPTED)
        generate_contract.delay(str(order.id))

    async def reject_order(self, order_id: UUID, user_id: UUID):
        order = await self.order_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError
        if order.lessor_id != user_id:
            raise NotLessorOrderError
        if order.status != OrderStatus.UNDER_CONSIDERATION:
            raise OrderStatusMustBeUnderConsiderationError
        await self.order_repository.update(order_id, status=OrderStatus.REJECTED)

        push = PushNotification(
            to_user_id=order.renter_id,
            title='К сожалению, вашу заявку на аренду отклонили(',
            body='Вашу заявку на аренду автомобиля отклонили \n Не отчаивайтесь и подберите новый вариант :)',
        )
        await self.notifications_kafka_producer.send_push_notification(push)

    async def cancel_order(self, order_id: UUID, user_id: UUID):
        order = await self.order_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError
        if order.renter_id != user_id:
            raise NotRenterOrderError
        if order.status != OrderStatus.UNDER_CONSIDERATION:
            raise OrderStatusMustBeUnderConsiderationError
        await self.order_repository.update(order_id, status=OrderStatus.CANCELED)

        push = PushNotification(
            to_user_id=order.lessor_id,
            title='Пользователь отменил заявку на аренду вашего авто',
            body='Пользователь отменил заявку на аренду вашего авто \n Не отчаивайтесь, уверены, скоро будет новая :)',
        )
        await self.notifications_kafka_producer.send_push_notification(push)
