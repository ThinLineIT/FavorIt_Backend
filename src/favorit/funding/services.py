from django.db import transaction

from favorit.funding.models import Funding, Product
from favorit.funding.schemas import CreateFundingRequestBody


class FundingCreator:
    def __init__(self, request_body: CreateFundingRequestBody, user_id):
        self.request_body = request_body
        self.user_id = user_id

    @transaction.atomic
    def create(self) -> Funding:
        product, _ = Product.objects.get_or_create(**self.request_body.product.dict())
        return Funding.objects.create(
            product=product, **self.request_body.dict(exclude={"product"}) | {"maker_id": self.user_id}
        )
