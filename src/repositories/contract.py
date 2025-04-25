from uuid import UUID

from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.db.models.contract import Contract


class ContractRepository(ISqlAlchemyRepository[Contract]):
    _model = Contract

    async def get_contract_obj_with_order(self, contract_id: UUID) -> Contract | None:
        query = select(Contract).options(selectinload(Contract.order)).where(Contract.id == contract_id)
        result = await self.session.execute(query)
        return result.scalars().first()
