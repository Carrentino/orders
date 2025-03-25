from uuid import UUID

from pydantic import BaseModel


class ContractResp(BaseModel):
    renter_signature: str | None
    lessor_signature: str | None
    order_id: UUID
    contract_url: str

    class Config:
        from_attributes = True


class SignContractByCodeReq(BaseModel):
    code: str
