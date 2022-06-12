from favorit.funding.models import Funding, Product
from favorit.funding.schemas import CreateFundingRequestBody


class FundingCreator:
    def __init__(self, request_body: CreateFundingRequestBody):
        self.request_body = request_body

    def create(self) -> Funding:
        product_data = self.request_body.product
        product, _ = Product.objects.get_or_create(**product_data.dict())
        return Funding.objects.create(product=product, **self.request_body.dict(exclude={"product"}))
