from http import HTTPStatus
from typing import Any

from django.conf import settings
from ninja.errors import HttpError

from favorit.funding.models import Funding, FundingAmount
from favorit.funding.schemas import CreateFundingRequestBody, PayFundingRequestBody
from favorit.funding.services import FundingCreator


def handle_create_funding(request_body: CreateFundingRequestBody) -> dict[str, Any]:
    funding_creator = FundingCreator(request_body=request_body)
    funding: Funding = funding_creator.create()
    return {"funding_id": funding.id, "product_link": funding.product.link}


def handle_retrieve_funding_detail(funding_id: int) -> dict[str, Any]:
    funding = Funding.objects.filter(id=funding_id).first()
    if funding is None:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message="펀딩이 존재 하지 않습니다.")

    return {
        "name": funding.name,
        "contents": funding.contents,
        "due_date": funding.due_date,
        "progress_percent": 0,  # 일단 0 percent로 세팅함
        "link_for_sharing": f"{settings.BASE_URL}/funding/{funding.id}",
        "product": {
            "link": funding.product.link,
            "option": funding.product.option,
            "price": funding.product.price,
        },
    }


def handle_close_funding(funding_id: int) -> dict[str, Any]:
    pass


def handle_pay_funding(funding_id: int, request_body: PayFundingRequestBody):
    funding = Funding.objects.filter(id=funding_id).first()
    funding_amount, _ = FundingAmount.objects.get_or_create(funding=funding)
    funding_amount.add_amount(request_body.amount)
