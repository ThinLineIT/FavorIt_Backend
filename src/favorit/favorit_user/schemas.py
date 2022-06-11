from typing import Any

from ninja import Field, Schema

from favorit.common.schemas import CommonErrorResponse, CommonResponse


class LoginRequest(Schema):
    kakao_token: str = Field(description="카카오 로그인 이후 받은 토큰")

    class Config:
        schema_extra = {"example": {"kakao_token": "some_kakao_token"}}


class LoginResponse(CommonResponse):
    data: dict[str, Any] = Field(description="API 사용을 위한 access token - JWT")

    class Config:
        schema_extra = {"example": {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3..."}}


class Login401ErrorResponse(CommonErrorResponse):
    detail: str