from typing import Any

from ninja import Field, Schema


class CommonResponse(Schema):
    data: dict[str, Any] = Field(description="클라이언트에 전달될 데이터")
    message: str = Field(description="고객에게 노출이 필요한 메세지", default="")


class CommonErrorResponse(Schema):
    detail: str = Field(description="에러에 대한 자세한 메세지")
    message: str = Field(description="고객에게 노출이 필요한 메세지", default="")
