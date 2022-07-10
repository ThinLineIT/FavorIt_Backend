from http import HTTPStatus
from typing import Any, Optional

import jwt
from django.conf import settings
from django.http import HttpRequest
from jwt import InvalidTokenError
from ninja.errors import HttpError
from ninja.security import HttpBearer

MSG_INVALID_TOKEN = "invalid token"


class FavorItAuth(HttpBearer):
    def __call__(self, request: HttpRequest) -> Optional[Any]:
        auth_result = super().__call__(request)
        if auth_result is None:
            raise HttpError(HTTPStatus.UNAUTHORIZED, MSG_INVALID_TOKEN)
        return auth_result

    def authenticate(self, request, token):
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
        except (InvalidTokenError, ValueError):
            raise HttpError(HTTPStatus.UNAUTHORIZED, MSG_INVALID_TOKEN)
        return payload


class FavorItAuthWithNoMember(HttpBearer):
    def __call__(self, request: HttpRequest) -> Optional[Any]:
        auth_result = super().__call__(request)
        if auth_result is None:
            return self.no_authenticate()
        return auth_result

    def authenticate(self, request, token):
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
        except (InvalidTokenError, ValueError):
            raise HttpError(HTTPStatus.UNAUTHORIZED, MSG_INVALID_TOKEN)
        return payload

    def no_authenticate(self):
        return {"user_id": None}
