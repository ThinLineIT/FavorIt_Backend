from ninja import Schema


class HelloWorldOut(Schema):
    hello: str
    world: str


class CreateBookResponse(Schema):
    name: str


class CreateBookRequestBody(Schema):
    name: str
