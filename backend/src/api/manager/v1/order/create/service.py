from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.manager.v1.logs.create.service import AuditLogService
from src.api.manager.v1.order.create.schemas import OrderCreate
from src.api.manager.v1.order.exceptions import EmptyOrder
from src.api.manager.v1.products.exceptions import ProductNotFound, ProductOutOfStock
from src.models.entities.order import Order
from src.models.entities.order_item import OrderItem
from src.models.entities.product import Product
from src.models.enums.action_type import ActionType
from src.models.enums.entity_type import EntityType


class OrderService:
    @staticmethod
    async def create(session: AsyncSession, order_data: OrderCreate):

        if not order_data.items:
            raise EmptyOrder()

        order = Order()
        session.add(order)

        product_ids = [item.product_external_id for item in order_data.items]

        result = await session.execute(
            select(Product).where(Product.external_id.in_(product_ids))
        )

        products = result.scalars().all()
        products_map = {p.external_id: p for p in products}

        order_items = []
        total_amount = Decimal("0.00")
        for item in order_data.items:
            product = products_map.get(item.product_external_id)

            if not product:
                raise ProductNotFound(
                    detail=f"Product {item.product_external_id} not found"
                )

            if product.stock_quantity < item.quantity:
                raise ProductOutOfStock(product.id)

        for item in order_data.items:
            product = products_map[item.product_external_id]

            product.stock_quantity -= item.quantity

            subtotal = product.price * item.quantity

            order_item = OrderItem(
                order=order,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
                subtotal=subtotal,
            )

            order_items.append(order_item)

            total_amount += subtotal

        order.total_amount = total_amount

        session.add_all(order_items)

        await AuditLogService.log(
            session,
            entity=EntityType.ORDER.value,
            action=ActionType.CREATE.value,
            entity_id=order.id,
            message=f"Order created with total {order.total_amount}",
        )

        await session.commit()
        await session.refresh(order)

        return order
