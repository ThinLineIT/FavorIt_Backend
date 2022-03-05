from ninja import Router

from bms.constants import MSG_BOOK_CREATED
from bms.handlers import handle_create_book
from bms.schemas import CreateBookRequestBody, CreateBookResponse

bms_router = Router(tags=["BMS"])


@bms_router.post(
    path="/book",
    url_name="create_book",
    summary="책 생성",
    description="책을 생성 합니다",
    response={201: CreateBookResponse},
    auth=None,
)
def create_book(request, request_body: CreateBookRequestBody):
    handle_create_book(request_body)
    return CreateBookResponse(message=MSG_BOOK_CREATED)
