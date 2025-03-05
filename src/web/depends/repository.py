from typing import Annotated

from fastapi import Depends
from helpers.depends.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.order import OrderRepository


async def get_order_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> OrderRepository:
    return OrderRepository(session=session)
