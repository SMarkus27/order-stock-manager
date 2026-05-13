from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.mixins.base import BaseMixin

if TYPE_CHECKING:
    from src.models.entities.order_item import OrderItem


class Product(BaseMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    stock_quantity: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
    )
