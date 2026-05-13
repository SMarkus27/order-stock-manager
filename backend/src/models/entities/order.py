from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.mixins.base import BaseMixin

if TYPE_CHECKING:
    from src.models.entities.order_item import OrderItem


class Order(BaseMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )
