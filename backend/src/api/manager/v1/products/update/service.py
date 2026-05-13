from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select

from src.api.manager.v1.logs.create.service import AuditLogService
from src.models.entities.product import Product
from src.models.enums.action_type import ActionType
from src.models.enums.entity_type import EntityType


class ProductUpdateService:
    @staticmethod
    async def update(session, product_id: UUID, new_data):

        query = select(Product).where(Product.external_id == product_id)
        result = await session.execute(query)
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        update_data = new_data.model_dump(exclude_unset=True)

        product.update(update_data)

        await AuditLogService.log(
            session,
            entity=EntityType.PRODUCT.value,
            action=ActionType.UPDATE.value,
            entity_id=product.id,
            message="Product updated",
        )

        await session.commit()
        await session.refresh(product)

        return product
