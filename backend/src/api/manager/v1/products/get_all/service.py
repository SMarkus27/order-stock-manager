from math import ceil

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.entities.product import Product


class ProductGetAllService:
    @staticmethod
    async def execute(
        session: AsyncSession,
        page: int = 1,
        per_page: int = 10,
    ):

        offset = (page - 1) * per_page

        total_query = select(func.count()).select_from(Product)

        total_result = await session.execute(total_query)

        total = total_result.scalar() or 0

        query = (
            select(Product)
            .offset(offset)
            .limit(per_page)
            .order_by(Product.created_at.desc())
        )

        result = await session.execute(query)

        products = result.scalars().all()

        pages = ceil(total / per_page) if total > 0 else 1

        return {
            "items": products,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
        }
