from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.manager.v1.order.create.schemas import OrderCreate
from src.api.manager.v1.order.create.service import OrderService
from src.config.session import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/orders")
async def create_order(
    order: OrderCreate,
    session: AsyncSession = Depends(get_db),
):
    return await OrderService.create(session, order)
