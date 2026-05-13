from decimal import Decimal
from http.client import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.manager.v1.logs.create.service import AuditLogService
from src.api.manager.v1.order.create.schemas import OrderCreate
from src.models.entities.order import Order
from src.models.entities.order_item import OrderItem
from src.models.entities.product import Product
from src.models.enums.action_type import ActionType
from src.models.enums.entity_type import EntityType


class OrderService:
    @staticmethod
    async def create(session: AsyncSession, order_data: OrderCreate):

        if not order_data.items:
            raise HTTPException(
                status_code=400, detail="Order must have at least one item"
            )

        order = Order()
        session.add(order)

        product_ids = [item.product_external_id for item in order_data.items]

        result = await session.execute(
            select(Product).where(Product.external_id.in_(product_ids))
        )

        products = result.scalars().all()
        products_map = {p.external_id: p for p in products}

        order_items = []
        total_amount = Decimal("0.00")  # 🔥 FIX

        for item in order_data.items:
            product = products_map.get(item.product_external_id)

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {item.product_external_id} not found",
                )

            if product.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product {product.id}",
                )

        for item in order_data.items:
            product = products_map[item.product_external_id]

            product.stock_quantity -= item.quantity

            subtotal = product.price * item.quantity  # 🔥 FIX TOTAL LINE

            order_item = OrderItem(
                order=order,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
                subtotal=subtotal,  # importante
            )

            order_items.append(order_item)

            total_amount += subtotal  # 🔥 acumulando total

        order.total_amount = total_amount  # 🔥 FIX FINAL

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
