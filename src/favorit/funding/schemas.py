from datetime import date
from typing import Any

from ninja import Field, Schema

from favorit.common.schemas import CommonErrorResponse, CommonResponse


class Product(Schema):
    link: str = Field(description="제품 링크")
    option: str = Field(description="제품 옵션")
    price: int = Field(description="제품 가격")


class CreateFundingRequestBody(Schema):
    name: str = Field(description="펀딩 이름")
    contents: str = Field(description="펀딩 내용")
    due_date: date = Field(description="펀딩 만료 기한")
    product: Product = Field(description="펀딩 제품")
    recipient_name: str = Field(description="수신자 이름")

    class Config:
        schema_extra = {
            "example": {
                "name": "윤권이의 생일선물은 아이패드로 부탁해",
                "contents": "궈니는 아이패드가 참 좋더라",
                "due_date": "2022-09-03",
                "product": {
                    "link": "https://www.apple.com/kr/shop/buy-ipad/ipad-air",
                    "option": "WIFI에 색상은 금색 256GB",
                    "price": 779000,
                },
                "recipient_name": "신윤권",
            }
        }


class CreateFundingResponse(CommonResponse):
    data: dict[str, Any]


class CreateFunding400ErrorResponse(CommonErrorResponse):
    detail: str = Field(default="fail creating funding")
