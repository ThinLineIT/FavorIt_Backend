from http import HTTPStatus

from ninja import Router

from favorit.debug.handlers import debug_handle_login
from favorit.debug.schemas import DebugLoginRequest
from favorit.favorit_user.schemas import Login401ErrorResponse, LoginResponse

debug_router = Router(tags=["Debug"])


@debug_router.post(
    path="/jwt",
    url_name="debug_jwt",
    summary="Debug를 위한 JWT를 반환 - no need access token in header",
    description="Debug를 위한 JWT를 반환 - 로그인 없이 JWT 사용을 위함",
    response={200: LoginResponse, 401: Login401ErrorResponse},
    auth=None,
)
def get_jwt(request, request_body: DebugLoginRequest):
    return HTTPStatus.OK, LoginResponse(data=debug_handle_login(request_body))
