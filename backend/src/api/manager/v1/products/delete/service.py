from sqlalchemy import UUID, select

from src.api.manager.v1.logs.create.service import AuditLogService
from src.api.manager.v1.products.exceptions import ProductNotFound
from src.models.entities.product import Product
from src.models.enums.action_type import ActionType
from src.models.enums.entity_type import EntityType


class ProductDeleteService:
    @staticmethod
    async def delete(session, product_external_id: UUID):

        query = select(Product).where(Product.external_id == product_external_id)
        result = await session.execute(query)
        product = result.scalar_one_or_none()

        if not product:
            raise ProductNotFound()

        await session.delete(product)

        await AuditLogService.log(
            session,
            entity=EntityType.PRODUCT.value,
            action=ActionType.DELETE.value,
            entity_id=product.id,
            message=f"Produto {product.name} deletado",
        )

        await session.commit()

        return {"message": "Produto deletado com Sucesso"}
