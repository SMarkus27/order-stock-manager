from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductListItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    external_id: UUID
    name: str
    sku: str
    price: Decimal
    stock_quantity: int
    created_at: datetime


class ProductPaginationResponse(BaseModel):
    items: list[ProductListItemSchema]

    total: int
    page: int
    per_page: int
    pages: int
