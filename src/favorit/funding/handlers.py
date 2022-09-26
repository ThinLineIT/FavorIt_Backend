from http import HTTPStatus
from typing import Any, Optional

from django.conf import settings
from ninja.errors import HttpError

from favorit.favorit_user.models import FavorItUser
from favorit.funding.enums import FundingState
from favorit.funding.models import Funding, FundingAmount, FundingPaymentResult
from favorit.funding.schemas import (
    CreateFundingRequestBody,
    PayFundingRequestBody,
    PaymentFundingRequest,
    VerifyBankAccountRequestBody,
)
from favorit.funding.services import FundingCreator
from favorit.integration.s3.client import S3Client


def handle_create_funding(request_body: CreateFundingRequestBody, user_id) -> dict[str, Any]:
    funding_creator = FundingCreator(request_body=request_body, user_id=user_id)
    funding: Funding = funding_creator.create()
    return {"funding_id": funding.id, "link_for_sharing": f"{settings.BASE_URL}/funding/{funding.id}"}


def handle_create_funding_v2(request_body: CreateFundingRequestBody, user_id, image) -> dict[str, Any]:
    funding_creator = FundingCreator(request_body=request_body, user_id=user_id)
    funding: Funding = funding_creator.create()

    s3_client = S3Client()
    s3_client.upload_file_object(image_data=image, bucket_path=f"funding/{funding.id}", content_type=image.content_type)

    return {"funding_id": funding.id, "link_for_sharing": f"{settings.BASE_URL}/funding/{funding.id}"}


def handle_retrieve_funding_detail(funding_id: int, user_id: Optional[int]) -> dict[str, Any]:
    # TODO: 여기에서 funding_id와 user_id를 통해서, maker와 방문한 user_id의 관계를 나타내는 테이블을 하나를 만들어서 저장해야한다
    """
    1. user_id가 funding_id에 접근한 형태임
    2. user_id의 친구 목록에 funding_id의 maker가 있는지 확인
    ---> 있으면, pass
    ---> 없으면, 친구로 추가
    """
    funding = Funding.objects.filter(id=funding_id).first()
    if funding is None:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message="펀딩이 존재 하지 않습니다.")

    user = FavorItUser.objects.get(id=user_id)
    if user_id != funding.maker.id and funding.maker.id not in user.friends.values_list("id", flat=True):
        user.friends.add(funding.maker.id)

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
            "price": funding.product.price,
        },
        "image": f"{settings.S3_BASE_URL}/funding/{funding.id}"
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


def handle_pay_funding_v2(funding_id: int, request_body: PayFundingRequestBody, image):
    funding = Funding.objects.filter(id=funding_id).first()
    funding_amount = FundingAmount.objects.create(funding=funding, amount=request_body.amount, from_name=request_body.from_name, to_name=request_body.to_name, contents=request_body.contents)

    s3_client = S3Client()
    s3_client.upload_file_object(image_data=image, bucket_path=f"presents/{funding_amount.id}", content_type=image.content_type)

    return {
        "funding_id": funding.id,
        "link_for_sharing": f"{settings.BASE_URL}/funding/{funding.id}",
        "link_for_uploaded": f"{settings.S3_BASE_URL}/presents/{funding_amount.id}"
    }


def handle_verify_bank_account(request_body: VerifyBankAccountRequestBody):
    if request_body.account_number != "91011112222":
        raise HttpError(HTTPStatus.BAD_REQUEST, "존재하지 않는 계좌번호입니다.")
    return {"account_owner_name": "홍길동"}


def handle_payment_funding(request_auth, request_body: PaymentFundingRequest):
    funding = Funding.objects.get(id=request_body.funding_id)
    if funding.maker.id != request_auth["user_id"]:
        raise HttpError(HTTPStatus.BAD_REQUEST, "펀딩 생성자가 아닙니다.")

    if funding.state != FundingState.CLOSED:
        raise HttpError(HTTPStatus.BAD_REQUEST, "펀딩이 닫힘 상태가 아닙니다")

    funding.state = FundingState.COMPLETED
    funding.save()
    funding_amount = FundingAmount.objects.filter(funding=funding).first()
    if funding_amount:
        price = funding_amount.amount
    else:
        price = 0
    FundingPaymentResult.objects.create(price=price, **request_body.dict())
