from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext
from starlette import status

from src.errors.http import NotOwnerOfContractHttpError, NotFoundContractHttpError, InvalidOrExpiredCodeHttpError
from src.errors.service import NotOwnerOfContractError, NotFoundContractError, InvalidOrExpiredCodeError
from src.services.contract import ContractService
from src.web.api.contracts.schems import ContractResp, SignContractByCodeReq
from src.web.depends.service import get_contract_service

contract_router = APIRouter()


@contract_router.get('/{contract_id}/', status_code=status.HTTP_200_OK)
async def get_contract(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    contract_service: Annotated[ContractService, Depends(get_contract_service)],
    contract_id: UUID,
) -> ContractResp:
    try:
        contract = await contract_service.get_contract(contract_id, UUID(current_user.user_id))
        return ContractResp(
            lessor_signature=contract.lessor_signature,
            renter_signature=contract.renter_signature,
            order_id=contract.order.id,
            contract_url=contract.file_link,
        )
    except NotOwnerOfContractError:
        raise NotOwnerOfContractHttpError from None
    except NotFoundContractError:
        raise NotFoundContractHttpError from None


@contract_router.post('/{contract_id}/send-code/', status_code=status.HTTP_204_NO_CONTENT)
async def send_email_code(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    contract_service: Annotated[ContractService, Depends(get_contract_service)],
    contract_id: UUID,
):
    try:
        await contract_service.send_email_code(contract_id, UUID(current_user.user_id))
    except NotOwnerOfContractError:
        raise NotOwnerOfContractHttpError from None
    except NotFoundContractError:
        raise NotFoundContractHttpError from None


@contract_router.post('/{contract_id}/sign-contract/', status_code=status.HTTP_204_NO_CONTENT)
async def sign_contract(
    current_user: Annotated[UserContext, Depends(get_current_user)],
    contract_service: Annotated[ContractService, Depends(get_contract_service)],
    contract_id: UUID,
    req_data: SignContractByCodeReq,
):
    try:
        await contract_service.sign_contract(contract_id, UUID(current_user.user_id), req_data)
    except NotOwnerOfContractError:
        raise NotOwnerOfContractHttpError from None
    except NotFoundContractError:
        raise NotFoundContractHttpError from None
    except InvalidOrExpiredCodeError:
        raise InvalidOrExpiredCodeHttpError from None
