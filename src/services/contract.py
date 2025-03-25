import hashlib
import random
import string
from uuid import UUID

from helpers.redis_client.client import RedisClient

from src.errors.service import NotOwnerOfContractError, NotFoundContractError, InvalidOrExpiredCodeError
from src.integrations.notifications import NotificationsKafkaProducer
from src.integrations.schemas import EmailMsg
from src.repositories.contract import ContractRepository
from src.settings import get_settings
from src.web.api.contracts.schems import SignContractByCodeReq


class ContractService:
    def __init__(
        self, contract_repository: ContractRepository, notifications_kafka_producer: NotificationsKafkaProducer
    ) -> None:
        self.contract_repository = contract_repository
        self.notifications_kafka_producer = notifications_kafka_producer

    async def get_contract(self, contract_id: UUID, user_id: UUID):
        contract = await self.contract_repository.get_contract_obj_with_order(contract_id)
        if not contract:
            raise NotFoundContractError
        if user_id not in {contract.order.lessor_id, contract.order.renter_id}:
            raise NotOwnerOfContractError
        return contract

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.digits, k=6))

    async def send_email_code(self, contract_id: UUID, user_id: UUID):
        contract = await self.contract_repository.get_contract_obj_with_order(contract_id)
        if not contract:
            raise NotFoundContractError
        if user_id not in {contract.order.lessor_id, contract.order.renter_id}:
            raise NotOwnerOfContractError
        code = self.generate_code()
        async with RedisClient(get_settings().redis.url, db=get_settings().redis.email_codes_db) as rc:
            await rc.set(f'{user_id!s}_{contract_id!s}', code, 300)
        email = EmailMsg(to_user_id=user_id, title='Код для подписания договора аренды', body=code)
        await self.notifications_kafka_producer.send_email(email)

    @staticmethod
    def generate_signature(code, user_id, contract_id) -> str:
        signature_data = f"{code}:{user_id}:{contract_id}".encode()
        return hashlib.sha256(signature_data).hexdigest()

    async def sign_contract(self, contract_id: UUID, user_id: UUID, req_data: SignContractByCodeReq):
        contract = await self.contract_repository.get_contract_obj_with_order(contract_id)
        if not contract:
            raise NotFoundContractError
        if user_id not in {contract.order.lessor_id, contract.order.renter_id}:
            raise NotOwnerOfContractError
        async with RedisClient(get_settings().redis.url, db=get_settings().redis.email_codes_db) as rc:
            code_from_redis = await rc.get(f'{user_id!s}_{contract_id!s}')
            if req_data.code != code_from_redis:
                raise InvalidOrExpiredCodeError
            signature = self.generate_signature(req_data.code, str(user_id), str(contract_id))
            if user_id == contract.order.lessor_id:
                await self.contract_repository.update(contract.id, lessor_signature=signature)
            else:
                await self.contract_repository.update(contract.id, renter_signature=signature)
