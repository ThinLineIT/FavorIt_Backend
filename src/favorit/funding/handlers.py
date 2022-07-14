from http import HTTPStatus
from typing import Any, Optional

from django.conf import settings
from ninja.errors import HttpError

from favorit.funding.enums import FundingState
from favorit.funding.models import Funding, FundingAmount
from favorit.funding.schemas import CreateFundingRequestBody, PayFundingRequestBody
from favorit.funding.services import FundingCreator


def handle_create_funding(request_body: CreateFundingRequestBody, user_id) -> dict[str, Any]:
    funding_creator = FundingCreator(request_body=request_body, user_id=user_id)
    funding: Funding = funding_creator.create()
    return {"funding_id": funding.id, "link_for_sharing": f"{settings.BASE_URL}/funding/{funding.id}"}


def handle_retrieve_funding_detail(funding_id: int, user_id: Optional[int]) -> dict[str, Any]:
    funding = Funding.objects.filter(id=funding_id).first()
    if funding is None:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message="펀딩이 존재 하지 않습니다.")

    funding_amount = FundingAmount.objects.filter(funding=funding).first()
    amount = funding_amount and funding_amount.amount
    return {
        "name": funding.name,
        "contents": funding.contents,
        "state": funding.state,
        "is_maker": user_id == funding.maker.id if user_id else False,
        "creation_date": funding.creation_date_format,
        "due_date": funding.due_date,
        "progress_percent": funding.progress_percent(amount or 0),
        "link_for_sharing": f"{settings.BASE_URL}/funding/{funding.id}",
        "product": {
            "link": funding.product.link,
            "option": funding.product.option,
            "price": funding.product.price,
        },
    }


def handle_close_funding(funding_id: int):
    funding = Funding.objects.get(id=funding_id)
    if not funding.enable_closed:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message="펀딩 상태를 변경할 수 없습니다")

    funding.change_state(state=FundingState.CLOSED)


def handle_pay_funding(funding_id: int, request_body: PayFundingRequestBody):
    funding = Funding.objects.filter(id=funding_id).first()
    funding_amount, _ = FundingAmount.objects.get_or_create(funding=funding)
    funding_amount.add_amount(request_body.amount)
    return {"funding_id": funding.id, "link_for_sharing": f"{settings.BASE_URL}/funding/{funding.id}"}
