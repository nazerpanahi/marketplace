from typing import *

from pydantic import Field

from .base import ExtendedBaseModel


class CreateProductInfo(ExtendedBaseModel):
    title: str
    price: float
    description: Optional[str]
    category: str
    city: str
    image: Optional[str]


class ProductInDB(CreateProductInfo):
    product_id: int = Field(..., alias='id', title='id')
