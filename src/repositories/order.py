from typing import Any
from uuid import UUID

from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select, desc, asc, func, and_, or_

from src.db.consts import OrderStatus
from src.db.models.order import Order
from src.web.api.orders.schems import CreateOrderReq


class OrderRepository(ISqlAlchemyRepository[Order]):
    _model = Order

    async def get_paginated_sorted_list(
        self,
        ids: list[UUID | int] | None = None,
        limit: int | None = 30,
        offset: int | None = 0,
        sort_by: str | None = None,
        sort_direction: str = 'asc',
        **filters: Any,
    ):
        query = select(self._model)

        query = query.where(self._model.id.in_(ids)) if ids else query
        query = query.filter_by(**filters) if filters else query

        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)

        if sort_by:
            column = getattr(self._model, sort_by, None)
            if column:
                query = query.order_by(desc(column)) if sort_direction == 'desc' else query.order_by(asc(column))
        query = query.limit(limit).offset(offset)
        db_objects = await self.session.scalars(query)
        objects = db_objects.all()
        return {
            'limit': limit,
            'offset': offset,
            'total': total,
            'data': objects,
        }

    async def intersection_orders_with_status_more_accepted(self, order_data: CreateOrderReq) -> list[Order]:
        start = order_data.desired_start_datetime
        finish = order_data.desired_finish_datetime
        orders = await self.session.execute(
            select(Order).where(
                and_(
                    or_(
                        and_(
                            start <= Order.desired_finish_datetime, finish >= Order.desired_finish_datetime
                        ),  # пересечение справа
                        and_(
                            start >= Order.desired_start_datetime, finish <= Order.desired_finish_datetime
                        ),  # новый полностью внутри
                        and_(
                            start <= Order.desired_start_datetime, finish >= Order.desired_start_datetime
                        ),  # пересечение слева
                    ),
                    Order.status == OrderStatus.ACCEPTED,
                )
            )
        )
        return orders.scalars().all()
