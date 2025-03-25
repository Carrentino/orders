import factory

from src.db.models.contract import Contract
from tests.factories.base import BaseSqlAlchemyFactory


class ContractFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = Contract

    filename = factory.Faker('word')
