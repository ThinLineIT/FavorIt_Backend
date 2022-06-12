from typing import Any

from favorit.funding.models import Funding
from favorit.funding.schemas import CreateFundingRequestBody
from favorit.funding.services import FundingCreator


def handle_create_funding(request_body: CreateFundingRequestBody) -> dict[str, Any]:
    funding_creator = FundingCreator(request_body=request_body)
    funding: Funding = funding_creator.create()
    return {"funding_id": funding.id}
