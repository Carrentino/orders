from pydantic import BaseModel, Field


class BasePaginatedQueryParams(BaseModel):
    page: int = Field(0, ge=0, description="Номер страницы")
    size: int = Field(10, ge=1, le=10, description="Размер страницы")


class BasePaginatedResp(BaseModel):
    page: int
    size: int
    total: int
    total_pages: int
