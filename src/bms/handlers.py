from bms.models import Book
from bms.schemas import CreateBookRequestBody


def handle_create_book(request_body: CreateBookRequestBody):
    Book.objects.create(**request_body.dict())
