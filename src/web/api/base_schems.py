from uuid import UUID

from pydantic import BaseModel, Field


class BasePaginatedQueryParams(BaseModel):
    limit: int = Field(30, ge=1, description="Количество")
    offset: int = Field(0, ge=0, description="Смещение")


class BasePaginatedResp(BaseModel):
    limit: int
    offset: int
    total: int


class BaseCreateObjResp(BaseModel):
    id: UUID
