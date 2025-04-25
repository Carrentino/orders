from httpx import AsyncClient
from starlette import status

from tests.factories.contract import ContractFactory
from tests.factories.order import OrderFactory


async def test_get_contract(auth_client: AsyncClient, session) -> None:
    contract = await ContractFactory.create()
    await session.flush()
    order = await OrderFactory.create(lessor_id=auth_client.user_id)
    order.contract_id = contract.id
    await session.commit()

    resp = await auth_client.get(f'api/contracts/{contract.id!s}/')
    assert resp.status_code == status.HTTP_200_OK
