from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.order import Order


class OrderRepository(ISqlAlchemyRepository[Order]):
    _model = Order
