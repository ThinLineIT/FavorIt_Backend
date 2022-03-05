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

    class Config:
        schema_extra = {
            "example": {
                "author_id": 1,
                "name": "리팩터링 워크북",
                "sub_name": "리팩토링을 더 잘해보자!",
                "type": "NEW_BOOK",
                "description": "이 책은 리팩토링 책과 보는 일종의 워크북이다",
                "published_at": "2022-03-05",
                "price": 13000,
                "sale_price": 10000,
                "published_at": "2022-03-05",
            }
        }
