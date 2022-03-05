from http import HTTPStatus

from ninja import Router

from bms.constants import MSG_BOOK_CREATED
from bms.handlers import handle_create_book, handle_retrieve_books
from bms.schemas import BookInfo, CreateBookRequestBody, CreateBookResponse

bms_router = Router(tags=["BMS"])


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
