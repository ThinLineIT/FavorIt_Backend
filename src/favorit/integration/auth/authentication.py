from http import HTTPStatus

import jwt
from django.conf import settings
from jwt import InvalidTokenError
from ninja.errors import HttpError
from ninja.security import HttpBearer


class FavorItAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
        except (InvalidTokenError, ValueError):
            raise HttpError(HTTPStatus.UNAUTHORIZED, "유효하지 않은 토큰 입니다.")
        return payload
