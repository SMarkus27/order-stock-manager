from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductUpdateInSchema(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None


class ProductUpdateInResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    external_id: UUID
    name: str
    sku: str
    price: Decimal
    stock_quantity: int
