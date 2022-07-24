from http import HTTPStatus

import jwt
from django.conf import settings
from jwt import DecodeError, exceptions
from ninja.errors import HttpError

from favorit.favorit_user.models import FavorItUser
from favorit.favorit_user.schemas import LoginRequest, RefreshTokenRequest
from favorit.favorit_user.services import AuthTokenPublisher
from favorit.integration.kakao.user_info_fetcher import KakaoUserInfoFetcher


def handle_login(request_body: LoginRequest) -> dict[str, str]:
    kakao_user_info_fetcher = KakaoUserInfoFetcher()
    kakao_user_info = kakao_user_info_fetcher.fetch(token=request_body.kakao_token)

    if kakao_user_info.get("id") is None:
        raise HttpError(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, message="카카오 유저 정보를 읽어오는데 실패 하였습니다")

    favorit_user, _ = FavorItUser.objects.get_or_create(kakao_user_id=kakao_user_info["id"])
    auth_token_publisher = AuthTokenPublisher(favorit_user=favorit_user)
    access_token, refresh_token = auth_token_publisher.publish()

    return {"access_token": access_token, "refresh_token": refresh_token}


def handle_refresh_token(request_body: RefreshTokenRequest) -> dict[str, str]:
    try:
        decoded = jwt.decode(request_body.refresh_token, settings.SECRET_KEY, ["HS256"])
    except (DecodeError, exceptions.ExpiredSignatureError):
        raise HttpError(status_code=HTTPStatus.UNAUTHORIZED, message="refresh token 형태가 올바르지 않습니다.")
    else:
        token_type = decoded["token_type"]
        favorit_user_id = decoded["user_id"]

    if token_type != "refresh":
        raise HttpError(status_code=HTTPStatus.UNAUTHORIZED, message="token의 payload 값이 유효하지 않습니다")

    favorit_user = FavorItUser.objects.filter(id=favorit_user_id).first()
    if favorit_user is None:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=f"user_id: {favorit_user}가 존재하지 않습니다")

    auth_token_publisher = AuthTokenPublisher(favorit_user=favorit_user)
    access_token, refresh_token = auth_token_publisher.publish()

    return {"access_token": access_token, "refresh_token": refresh_token}
