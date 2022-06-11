from http import HTTPStatus

from ninja import Path, Router
from ninja.errors import HttpError

from favorit.funding.constants import MSG_BOOK_CREATED
from favorit.funding.enums import BookType
from favorit.funding.models import Book
from favorit.funding.schemas import (
    BookInfoResponse,
    CreateBookRequestBody,
    CreateBookResponse,
    OptionListResponse,
)

bms_router = Router(tags=["BMS"])
bms_options_router = Router(tags=["BMS 옵션 리스트"])


@bms_router.get(
    path="/books",
    url_name="books",
    summary="책 리스트",
    description="등록된 책 리스트를 보여줍니다",
    response={200: list[BookInfoResponse]},
    auth=None,
)
def retrieve_books(request):
    return HTTPStatus.OK, [BookInfoResponse.from_orm(book) for book in Book.objects.all()]


@bms_router.get(
    path="/books/{book_id}",
    url_name="books",
    summary="책 상세 정보",
    description="등록된 책 상세 정보를 보여줍니다",
    response={200: BookInfoResponse},
    auth=None,
)
def retrieve_book(request, book_id: int = Path(...)):
    book = Book.objects.filter(id=book_id).first()
    if book is None:
        raise HttpError(HTTPStatus.BAD_REQUEST, "존재 하지 않는 책 입니다.")
    return HTTPStatus.OK, BookInfoResponse.from_orm(book)


@bms_options_router.get(
    path="/book-types",
    url_name="book_types_option_list",
    summary="책의 타입 옵션 리스트",
    description="책 타입의 옵션 리스트를 보여줍니다",
    response={200: list[OptionListResponse]},
    auth=None,
)
def retrieve_book_types_option_list(request):
    return HTTPStatus.OK, BookType.as_options()


@bms_router.post(
    path="/books",
    url_name="books",
    summary="책 생성",
    description="책을 생성 합니다",
    response={201: CreateBookResponse},
    auth=None,
)
def create_book(request, request_body: CreateBookRequestBody):
    Book.objects.create(**request_body.dict())
    return HTTPStatus.CREATED, CreateBookResponse(message=MSG_BOOK_CREATED)
