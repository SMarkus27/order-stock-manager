from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.manager.v1.products.create.schemas import (
    ProductCreateInSchema,
    ProductCreateResponse,
)
from src.api.manager.v1.products.create.service import ProductCreateService
from src.api.manager.v1.products.delete.service import ProductDeleteService
from src.api.manager.v1.products.get.schemas import ProductGetOneResponse
from src.api.manager.v1.products.get.service import ProductGetService
from src.api.manager.v1.products.get_all.schemas import ProductPaginationResponse
from src.api.manager.v1.products.get_all.service import ProductGetAllService
from src.api.manager.v1.products.update.schemas import (
    ProductUpdateInResponse,
    ProductUpdateInSchema,
)
from src.api.manager.v1.products.update.service import ProductUpdateService
from src.config.session import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "/",
    response_model=ProductCreateResponse,
)
async def create_product(
    product: ProductCreateInSchema,
    db: AsyncSession = Depends(get_db),
):
    return await ProductCreateService.create(
        session=db,
        product=product,
    )


@router.get("/{product_external_id}", response_model=ProductGetOneResponse)
async def get_product(product_external_id: UUID, db: AsyncSession = Depends(get_db)):
    return await ProductGetService.get(
        session=db, product_external_id=product_external_id
    )


@router.get(
    "/",
    response_model=ProductPaginationResponse,
)
async def get_products(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    return await ProductGetAllService.execute(
        session=session,
        page=page,
        per_page=per_page,
    )


@router.patch("/{product_external_id}", response_model=ProductUpdateInResponse)
async def update_product(
    product_external_id: UUID,
    new_data: ProductUpdateInSchema,
    session: AsyncSession = Depends(get_db),
):
    return await ProductUpdateService.update(session, product_external_id, new_data)


@router.delete("/{product_external_id}")
async def delete_product(
    product_external_id: UUID, session: AsyncSession = Depends(get_db)
):
    return await ProductDeleteService.delete(session, product_external_id)
