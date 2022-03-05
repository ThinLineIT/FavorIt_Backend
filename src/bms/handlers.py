from bms.models import Book
from bms.schemas import CreateBookResponse


def handle_create_book(name: str):
    Book.objects.create(name=name)
    return CreateBookResponse(name="my book")
