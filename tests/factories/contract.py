import factory

from src.db.models.contract import Contract
from tests.factories.base import BaseSqlAlchemyFactory


class ContractFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = Contract

    url = factory.Faker('url')
    renter_signature = factory.Faker('sha256')
    lessor_signature = factory.Faker('sha256')
