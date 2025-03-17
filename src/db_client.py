from functools import lru_cache

from helpers.sqlalchemy.client import SQLAlchemyClient
from pydantic import PostgresDsn

from src.settings import get_settings


@lru_cache
def make_db_client(dsn: PostgresDsn = get_settings().postgres_dsn) -> SQLAlchemyClient:
    return SQLAlchemyClient(dsn=dsn)
