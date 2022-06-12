from http import HTTPStatus

from ninja import Router

from favorit.funding.handlers import handle_create_funding
from favorit.funding.schemas import (
    CreateFunding400ErrorResponse,
    CreateFundingRequestBody,
    CreateFundingResponse,
)

funding_router = Router(tags=["Funding"])


@funding_router.post(
    path="/funding",
    url_name="create_funding",
    summary="펀딩 생성",
    description="펀딩을 생성 합니다",
    response={201: CreateFundingResponse, 400: CreateFunding400ErrorResponse},
    auth=None,
)
def create_funding(request, request_body: CreateFundingRequestBody):
    return HTTPStatus.CREATED, CreateFundingResponse(data=handle_create_funding(request_body))
