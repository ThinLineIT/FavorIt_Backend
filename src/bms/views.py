from ninja import Router

from bms.handlers import handle_create_book
from bms.schemas import CreateBookRequestBody, CreateBookResponse, HelloWorldOut

bms_router = Router(tags=["BMS"])


@bms_router.get(
    path="/hello", url_name="hello_world", summary="hello world!!12312312", response=HelloWorldOut, auth=None
)
def hello(request):
    return {"hello": "hello", "world": "world"}


@bms_router.post(
    path="/book",
    url_name="create_book",
    summary="책 생성",
    description="책을 생성 합니다",
    response={201: CreateBookResponse},
    auth=None,
)
def create_book(request, request_body: CreateBookRequestBody):
    return handle_create_book(request_body)
