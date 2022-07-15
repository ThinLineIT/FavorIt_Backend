from datetime import date

from ninja import Field, Schema

from favorit.common.schemas import CommonErrorResponse, CommonResponse
from favorit.funding.enums import BankEnum, FundingState


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


class CreatingFundingResponseSchema(Schema):
    funding_id: int
    link_for_sharing: str


class CreateFundingResponse(Schema):
    data: CreatingFundingResponseSchema
    message: str = Field(description="고객에게 노출이 필요한 메세지", default="")


class CreateFunding400ErrorResponse(CommonErrorResponse):
    detail: str = Field(default="fail creating funding")


class FundingDetailResponseSchema(Schema):
    name: str
    contents: str
    state: FundingState
    is_maker: bool
    creation_date: date
    due_date: date
    progress_percent: int
    link_for_sharing: str
    product: Product


class RetrievingFundingDetailResponse(Schema):
    data: FundingDetailResponseSchema
    message: str = Field(description="고객에게 노출이 필요한 메세지", default="")

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


class PayFundingResponseSchema(Schema):
    funding_id: int
    link_for_sharing: str


class PayFundingResponse(Schema):
    data: PayFundingResponseSchema
    message: str = Field(description="고객에게 노출이 필요한 메세지", default="")


class BankOptionListResponse(Schema):
    text: str
    value: str
    image: str

    class Config:
        schema_extra = {
            "example": {
                "text": "신한",
                "value": "SHINHAN",
                "image": "https://s3-favorit-dev.s3.ap-northeast-2.amazonaws.com/bank/shinhan.png",
            }
        }


class VerifyBankAccountRequestBody(Schema):
    bank_code: BankEnum
    account_number: str

    class Config:
        schema_extra = {"example": {"bank_code": "NH", "account_number": "91011112222"}}


class VerifyBankAccountResponseSchema(Schema):
    account_owner_name: str

    class Config:
        schema_extra = {
            "example": {
                "account_owner_name": "홍길동",
            }
        }


class VerifyBankAccountResponse(Schema):
    data: VerifyBankAccountResponseSchema
    message: str = Field(description="고객에게 노출이 필요한 메세지", default="")
