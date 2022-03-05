from http import HTTPStatus

from bms.constants import MSG_BOOK_CREATED
from bms.enums import BookType
from bms.handlers import handle_create_book, handle_retrieve_books
from bms.schemas import (
    BookInfo,
    CreateBookRequestBody,
    CreateBookResponse,
    OptionListResponse,
)
from config.routers import bms_options_router, bms_router


@bms_router.get(
    path="/books",
    url_name="books",
    summary="책 리스트",
    description="등록된 책 리스트를 보여줍니다",
    response={200: list[BookInfo]},
    auth=None,
)
def retrieve_books(request):
    return HTTPStatus.OK, handle_retrieve_books()


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
    handle_create_book(request_body)
    return HTTPStatus.CREATED, CreateBookResponse(message=MSG_BOOK_CREATED)
