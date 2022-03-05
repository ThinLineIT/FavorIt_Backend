from ninja import Schema


class HelloWorldOut(Schema):
    hello: str
    world: str
