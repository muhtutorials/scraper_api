from uuid import UUID

from pydantic import BaseModel, root_validator

from .utils import uuid1_time_to_datetime


class ProductCreateSchema(BaseModel):
    url: str


class ProductSchema(BaseModel):
    asin: str
    url: str
    title: str
    price: int


class ProductScrapeSchema(BaseModel):
    uuid: UUID
    asin: str
    url: str
    title: str
    price: int
    created_at: str

    @root_validator(pre=True)
    def add_timestamp(cls, values):
        values['created_at'] = uuid1_time_to_datetime(values['uuid'].time).strftime('%Y-%m-%d %H:%M:%S')
        return values
