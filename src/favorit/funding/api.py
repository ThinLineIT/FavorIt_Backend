from http import HTTPStatus

from ninja import Path, Router

from favorit.funding.enums import BankEnum
from favorit.funding.handlers import (
    handle_close_funding,
    handle_create_funding,
    handle_pay_funding,
    handle_payment_funding,
    handle_retrieve_funding_detail,
    handle_verify_bank_account,
)
from favorit.funding.schemas import (
    BankOptionListResponse,
    CloseFundingResponse,
    CreateFunding400ErrorResponse,
    CreateFundingRequestBody,
    CreateFundingResponse,
    CreatingFundingResponseSchema,
    FundingDetailResponseSchema,
    PayFundingRequestBody,
    PayFundingResponse,
    PayFundingResponseSchema,
    PaymentFundingRequest,
    PaymentFundingResponse,
    RetrievingFundingDetailResponse,
    VerifyBankAccountRequestBody,
    VerifyBankAccountResponse,
    VerifyBankAccountResponseSchema,
)
from favorit.integration.auth.authentication import FavorItAuth, FavorItAuthWithNoMember

funding_router = Router(tags=["Funding"])


@funding_router.post(
    path="/funding",
    url_name="create_funding",
    summary="펀딩 생성 - token required",
    description="펀딩을 생성 합니다",
    response={201: CreateFundingResponse, 400: CreateFunding400ErrorResponse},
    auth=FavorItAuth(),
)
def create_funding(request, request_body: CreateFundingRequestBody):
    user_id = request.auth["user_id"]
    return HTTPStatus.CREATED, CreateFundingResponse(
        data=CreatingFundingResponseSchema(**handle_create_funding(request_body, user_id))
    )


@funding_router.get(
    path="/funding/{funding_id}",
    url_name="retrieve_funding_detail",
    summary="펀딩 상세 - token optional",
    description="펀딩상세 정보를 보여줍니다 - 회원의 경우에는 token이 필요하고, 비회원의 경우는 token이 필요하지 않습니다",
    response={200: RetrievingFundingDetailResponse},
    auth=FavorItAuthWithNoMember(),
)
def retrieve_funding_detail(request, funding_id: int = Path(...)):
    if payload := request.auth:
        user_id = payload["user_id"]
    else:
        user_id = None
    return HTTPStatus.OK, RetrievingFundingDetailResponse(
        data=FundingDetailResponseSchema(**handle_retrieve_funding_detail(funding_id, user_id))
    )


@funding_router.post(
    path="/funding/{funding_id}/close",
    url_name="close_funding",
    summary="펀딩 마감 - token required",
    description="생성한 펀딩을 마감 합니다",
    response={200: CloseFundingResponse},
    auth=FavorItAuth(),
)
def close_funding(request, funding_id: int = Path(...)):
    handle_close_funding(funding_id)
    return HTTPStatus.OK, CloseFundingResponse(data="")


@funding_router.post(
    path="/funding/{funding_id}/present",
    url_name="pay_funding",
    summary="선물 하기 - token required",
    description="펀딩 제품의 가격을 결제 합니다",
    response={200: PayFundingResponse},
    auth=FavorItAuth(),
)
def pay_funding(request, request_body: PayFundingRequestBody, funding_id: int = Path(...)):
    return HTTPStatus.OK, PayFundingResponse(
        data=PayFundingResponseSchema(**handle_pay_funding(funding_id, request_body))
    )


@funding_router.post(
    path="/funding/options/bank",
    url_name="bank_option_list",
    summary="은행 옵션 리스트 - token required",
    description="은행 옵션 리스트를 리턴 합니다",
    response={200: list[BankOptionListResponse]},
    auth=FavorItAuth(),
)
def retrieve_bank_option_list(request):
    return HTTPStatus.OK, [BankOptionListResponse(**bank) for bank in BankEnum.option_list()]


@funding_router.post(
    path="/funding/verification/bank-account",
    url_name="verification_bank_account",
    summary="예금계좌 조회 - token required",
    description="예금계좌를 조회 합니다",
    response={200: VerifyBankAccountResponse},
    auth=FavorItAuth(),
)
def verify_bank_account(request, request_body: VerifyBankAccountRequestBody):
    return HTTPStatus.OK, VerifyBankAccountResponse(
        data=VerifyBankAccountResponseSchema(**handle_verify_bank_account(request_body))
    )


@funding_router.post(
    path="/funding/{funding_id}/payment",
    url_name="payment_funding",
    summary="펀딩 정산 - token required",
    description="펀딩된 금액을 정산 받습니다",
    response={200: PaymentFundingResponse},
    auth=FavorItAuth(),
)
def payment_funding(request, request_body: PaymentFundingRequest):
    handle_payment_funding(request.auth, request_body)
    return HTTPStatus.OK, PaymentFundingResponse(data="")
