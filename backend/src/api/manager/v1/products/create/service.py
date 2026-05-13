from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.manager.v1.logs.create.service import AuditLogService
from src.api.manager.v1.products.create.schemas import ProductCreateInSchema
from src.models.entities.product import Product
from src.models.enums.action_type import ActionType
from src.models.enums.entity_type import EntityType


class ProductCreateService:
    @staticmethod
    async def create(session: AsyncSession, product: ProductCreateInSchema):

        query = select(Product).where(Product.sku == product.sku)
        result = await session.execute(query)
        existing_product = result.scalar_one_or_none()

        if existing_product:
            raise HTTPException(status_code=400, detail="Product already exists")

        new_product = Product(**product.model_dump())

        session.add(new_product)

        await AuditLogService.log(
            session,
            entity=EntityType.PRODUCT.value,
            action=ActionType.CREATE.value,
            entity_id=new_product.id,
            message=f"Product {product.name} created",
        )

        await session.commit()

        await session.refresh(new_product)

        return new_product
