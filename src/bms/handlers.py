from bms.models import Book
from bms.schemas import BookInfo, CreateBookRequestBody


def handle_create_book(request_body: CreateBookRequestBody):
    Book.objects.create(**request_body.dict())


def handle_retrieve_books() -> list[BookInfo]:
    books = Book.objects.all()
    return [
        BookInfo(
            id=book.id,
            author=book.author.name,
            name=book.name,
            sub_name=book.sub_name,
            type=book.type,
            description=book.description,
            published_at=book.published_at,
            price=book.price,
            sale_price=book.sale_price,
            purchased_at=book.purchased_at,
        )
        for book in books
    ]
