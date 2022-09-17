from typing import *

from pydantic import Field

from .base import ExtendedBaseModel


class Category(ExtendedBaseModel):
    title: str
    description: Optional[str]


class CategoryInDB(Category):
    category_id: int = Field(..., alias='id', title='id')
