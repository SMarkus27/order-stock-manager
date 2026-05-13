from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.entities.product import Product


class ProductGetService:
    @staticmethod
    async def get(session: AsyncSession, product_external_id: UUID):
        query = select(Product).where(Product.external_id == product_external_id)

        result = await session.execute(query)
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )
        return product
