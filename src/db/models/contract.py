from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.sqlalchemy.base_model import Base

from src.settings import get_settings

if TYPE_CHECKING:
    from src.db.models.order import Order


class Contract(Base):
    __tablename__ = 'contracts'

    filename: Mapped[str]
    renter_signature: Mapped[str] = mapped_column(String, nullable=True)
    lessor_signature: Mapped[str] = mapped_column(String, nullable=True)
    order: Mapped['Order'] = relationship("Order", back_populates="contract", uselist=False)

    @property
    def file_link(self):
        return get_settings().storage.get_path(self.filename)
