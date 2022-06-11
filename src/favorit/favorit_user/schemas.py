from typing import Any

from ninja import Field, Schema

from favorit.common.schemas import CommonResponse


class LoginRequest(Schema):
    kakao_token: str = Field(description="카카오 로그인 이후 받은 토큰")


class LoginResponse(CommonResponse):
    data: dict[str, Any] = Field(description="API 사용을 위한 access token - JWT")

    class Config:
        schema_extra = {"example": {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3..."}}


class Login401ErrorResponse(Schema):
    detail: str
