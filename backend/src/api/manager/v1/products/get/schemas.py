from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductGetOneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    external_id: UUID
    name: str
    sku: str
    price: Decimal
    stock_quantity: int
