from typing import Any

from favorit.funding.models import Funding
from favorit.funding.schemas import CreateFundingRequestBody, PayFundingRequestBody
from favorit.funding.services import FundingCreator


def handle_create_funding(request_body: CreateFundingRequestBody) -> dict[str, Any]:
    funding_creator = FundingCreator(request_body=request_body)
    funding: Funding = funding_creator.create()
    return {"funding_id": funding.id, "product_link": funding.product.link}


def handle_retrieve_funding_detail(funding_id: int) -> dict[str, Any]:
    return {
        "name": "윤권이의 생일선물은 아이패드로 부탁해",
        "contents": "궈니는 아이패드가 참 좋더라",
        "due_date": "2022-09-03",
        "progress_percent": 33,
        "link_for_sharing": "https://www.favorit.com/funding/1001",
        "product": {
            "link": "https://www.apple.com/kr/shop/buy-ipad/ipad-air",
            "option": "WIFI에 색상은 금색 256GB",
            "price": 779000,
        },
    }


def handle_close_funding(funding_id: int) -> dict[str, Any]:
    pass


def handle_pay_funding(funding_id: int, request_body: PayFundingRequestBody) -> dict[str, Any]:
    pass
