from http import HTTPStatus

from ninja import Router

from favorit.favorit_user.schemas import (
    Login401ErrorResponse,
    LoginRequest,
    LoginResponse,
)

auth_router = Router(tags=["Auth"])


@auth_router.post(
    path="/login",
    url_name="login",
    summary="로그인을 위한 JWT를 반환",
    description="로그인을 위한 JWT를 반환합니다. 추후에 refresh token 추가 예정",
    response={200: LoginResponse, 401: Login401ErrorResponse},
    auth=None,
)
def login(request, request_body: LoginRequest):
    return HTTPStatus.OK, LoginResponse(data={"access_token": "test_access_token"})
