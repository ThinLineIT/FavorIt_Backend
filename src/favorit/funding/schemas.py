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
            }
        }


class CreateFundingResponse(CommonResponse):
    data: dict[str, Any]


class CreateFunding400ErrorResponse(CommonErrorResponse):
    detail: str = Field(default="fail creating funding")


class RetrievingFundingDetailResponse(CommonResponse):
    pass

    class Config:
        schema_extra = {
            "example": {
                "data": {
                    "name": "윤권이의 생일선물은 아이패드로 부탁해",
                    "contents": "궈니는 아이패드가 참 좋더라",
                    "state": "OPENED",
                    "is_maker": True,
                    "due_date": "2022-09-03",
                    "progress_percent": 33,
                    "link_for_sharing": "https://www.favorit.com/funding/1001",
                    "product": {
                        "link": "https://www.apple.com/kr/shop/buy-ipad/ipad-air",
                        "option": "WIFI에 색상은 금색 256GB",
                        "price": 779000,
                    },
                },
                "message": "",
            }
        }


class CloseFundingResponse(CommonResponse):
    pass


class PayFundingRequestBody(Schema):
    amount: int = Field(description="선물하기 결제 금액")

    class Config:
        schema_extra = {
            "example": {
                "amount": 570000,
            }
        }


class PayFundingResponse(CommonResponse):
    pass
