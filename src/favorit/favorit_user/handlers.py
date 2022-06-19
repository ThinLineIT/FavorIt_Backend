from http import HTTPStatus

import jwt
from django.conf import settings
from jwt import DecodeError
from ninja.errors import HttpError

from favorit.favorit_user.schemas import LoginRequest, RefreshTokenRequest
from favorit.favorit_user.services import get_auth_tokens
from favorit.integration.kakao.user_info_fetcher import KakaoUserInfoFetcher


def handle_login(request_body: LoginRequest) -> dict[str, str]:
    kakao_user_info_fetcher = KakaoUserInfoFetcher()
    kakao_user_info = kakao_user_info_fetcher.fetch(token=request_body.kakao_token)

    if kakao_user_info.get("id") is None:
        raise HttpError(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, message="카카오 유저 정보를 읽어오는데 실패 하였습니다")

    access_token, refresh_token = get_auth_tokens(kakao_user_id=kakao_user_info["id"])
    return {"access_token": access_token, "refresh_token": refresh_token}


def handle_refresh_token(request_body: RefreshTokenRequest) -> dict[str, str]:
    try:
        decoded = jwt.decode(request_body.access_token, settings.SECRET_KEY, ["HS256"])
    except DecodeError:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message="access token 형태가 올바르지 않습니다.")
    else:
        kaka_user_id = decoded["user_id"]

    access_token, refresh_token = get_auth_tokens(kakao_user_id=kaka_user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}
