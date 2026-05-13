from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.mixins.base import BaseMixin

if TYPE_CHECKING:
    from src.models.entities.order import Order
    from src.models.entities.product import Product


class OrderItem(BaseMixin):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        back_populates="order_items",
    )
