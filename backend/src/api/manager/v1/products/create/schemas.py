from decimal import Decimal
from typing import TypedDict
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductCreateInSchema(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
    )

    sku: str = Field(
        min_length=1,
        max_length=100,
    )

    price: Decimal = Field(
        gt=0,
    )

    stock_quantity: int = Field(
        ge=0,
    )


class ProductCreateInDict(TypedDict):
    name: str
    sku: str
    price: Decimal
    stock_quantity: int


class ProductCreateResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    external_id: UUID
