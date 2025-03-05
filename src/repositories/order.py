from typing import Any
from uuid import UUID

from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select, desc, asc

from src.db.models.order import Order


class OrderRepository(ISqlAlchemyRepository[Order]):
    _model = Order

    async def get_paginated_sorted_list(
        self,
        ids: list[UUID | int] | None = None,
        page: int | None = None,
        size: int | None = None,
        sort_by: str | None = None,
        sort_direction: str = 'asc',
        **filters: Any,
    ):
        query = select(self._model)

        query = query.where(self._model.id.in_(ids)) if ids else query
        query = query.filter_by(**filters) if filters else query

        if sort_by:
            column = getattr(self._model, sort_by, None)
            if column:
                query = query.order_by(desc(column)) if sort_direction == 'desc' else query.order_by(asc(column))
        offset_min = page * size
        offset_max = (page + 1) * size

        db_objects = await self.session.scalars(query)
        objects = db_objects.all()
        return {
            'page': page,
            'size': size,
            'total': len(objects),
            'data': objects[offset_min:offset_max],
        }
