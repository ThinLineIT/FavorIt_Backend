from bms.constants import MSG_BOOK_CREATED
from bms.models import Book
from bms.schemas import CreateBookRequestBody, CreateBookResponse


def handle_create_book(request_body: CreateBookRequestBody):
    Book.objects.create(**request_body.dict())
    return CreateBookResponse(message=MSG_BOOK_CREATED)
