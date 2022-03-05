from ninja import Router

from bms.schemas import HelloWorldOut

bms_router = Router(tags=["BMS"])


@bms_router.get(
    path="/hello", url_name="hello_world", summary="hello world!!12312312", response=HelloWorldOut, auth=None
)
def hello(request):
    return {"hello": "hello", "world": "world"}
