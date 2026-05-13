from uuid import UUID

from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_external_id: UUID
    quantity: int


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]
