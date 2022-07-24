from http import HTTPStatus

from ninja import Router

from favorit.favorit_user.handlers import handle_login, handle_refresh_token
from favorit.favorit_user.schemas import (
    Login401ErrorResponse,
    LoginRequest,
    LoginResponse,
    RefreshToken400ErrorResponse,
    RefreshToken401ErrorResponse,
    RefreshTokenRequest,
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
    return HTTPStatus.OK, LoginResponse(data=handle_login(request_body))


@auth_router.post(
    path="/refresh-token",
    url_name="refresh_token",
    summary="refresh token을 발행",
    description="refresh token을 발행 합니다.",
    response={200: LoginResponse, 400: RefreshToken400ErrorResponse, 401: RefreshToken401ErrorResponse},
    auth=None,
)
def refresh_token(request, request_body: RefreshTokenRequest):
    return HTTPStatus.OK, LoginResponse(data=handle_refresh_token(request_body))
