from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.manager.v1.products.exceptions import ProductNotFound
from src.models.entities.product import Product


class ProductGetService:
    @staticmethod
    async def get(session: AsyncSession, product_external_id: UUID):
        query = select(Product).where(Product.external_id == product_external_id)

        result = await session.execute(query)
        product = result.scalar_one_or_none()
        if not product:
            raise ProductNotFound()
        return product
