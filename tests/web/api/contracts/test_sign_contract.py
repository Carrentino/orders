import hashlib
from unittest.mock import patch, AsyncMock

from httpx import AsyncClient
from starlette import status

from tests.factories.contract import ContractFactory
from tests.factories.order import OrderFactory


@patch('helpers.redis_client.client.RedisClient.__aenter__', new_callable=AsyncMock)
async def test_sign_contract(mock_redis: AsyncMock, auth_client: AsyncClient, session) -> None:
    mock_redis_instance = AsyncMock()
    mock_redis.return_value = mock_redis_instance
    code = "123"
    mock_redis_instance.get.return_value = code
    contract = await ContractFactory.create()
    await session.flush()
    order = await OrderFactory.create(lessor_id=auth_client.user_id)
    order.contract_id = contract.id
    await session.commit()

    resp = await auth_client.post(f'api/contracts/{contract.id!s}/sign-contract/', json={'code': code})
    signature_data = f"{code}:{auth_client.user_id!s}:{contract.id!s}".encode()
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    await session.flush()
    await session.refresh(contract)
    assert contract.lessor_signature == hashlib.sha256(signature_data).hexdigest()
