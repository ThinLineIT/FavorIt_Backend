from http import HTTPStatus

from ninja import Path, Router

from favorit.funding.handlers import (
    handle_close_funding,
    handle_create_funding,
    handle_pay_funding,
    handle_retrieve_funding_detail,
)
from favorit.funding.schemas import (
    CloseFundingResponse,
    CreateFunding400ErrorResponse,
    CreateFundingRequestBody,
    CreateFundingResponse,
    CreatingFundingResponseSchema,
    FundingDetailResponseSchema,
    PayFundingRequestBody,
    PayFundingResponse,
    PayFundingResponseSchema,
    RetrievingFundingDetailResponse,
)
from favorit.integration.auth.authentication import FavorItAuth, FavorItAuthWithNoMember

funding_router = Router(tags=["Funding"])


@funding_router.post(
    path="/funding",
    url_name="create_funding",
    summary="펀딩 생성 - need access token in header",
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
    summary="펀딩 상세 - need access token in header or not",
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
    summary="펀딩 마감 - need access token in header",
    description="생성한 펀딩을 마감 합니다",
    response={200: CloseFundingResponse},
    auth=FavorItAuth(),
)
def close_funding(request, funding_id: int = Path(...)):
    handle_close_funding(funding_id)
    return HTTPStatus.OK, CloseFundingResponse(data="")


@funding_router.post(
    path="/funding/{funding_id}/payment",
    url_name="pay_funding",
    summary="선물 하기 - need access token in header",
    description="펀딩 제품의 가격을 결제 합니다",
    response={200: PayFundingResponse},
    auth=FavorItAuth(),
)
def pay_funding(request, request_body: PayFundingRequestBody, funding_id: int = Path(...)):
    return HTTPStatus.OK, PayFundingResponse(
        data=PayFundingResponseSchema(**handle_pay_funding(funding_id, request_body))
    )
