from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from helpers.sqlalchemy.base_model import Base


class Contract(Base):
    __tablename__ = 'contracts'

    url: Mapped[str] = mapped_column(String)
    renter_signature: Mapped[str | None] = mapped_column(String, nullable=True)
    lessor_signature: Mapped[str | None] = mapped_column(String, nullable=True)
