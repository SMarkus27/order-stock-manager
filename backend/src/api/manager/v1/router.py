from fastapi import APIRouter

from src.api.manager.v1.order.controller import router as orders_router
from src.api.manager.v1.products.controller import router as products_router

router = APIRouter(prefix="/v1")

router.include_router(products_router)
router.include_router(orders_router)
