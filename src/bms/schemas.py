from datetime import date

from ninja import Schema

from bms.enums import BookType


class HelloWorldOut(Schema):
    hello: str
    world: str


class DefaultSchema(Schema):
    message: str


class CreateBookResponse(DefaultSchema):
    pass


class CreateBookRequestBody(Schema):
    author_id: int
    name: str
    sub_name: str
    type: BookType
    description: str
    published_at: date
    price: int
    sale_price: int
    purchased_at: date
