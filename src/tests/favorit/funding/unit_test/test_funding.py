import pytest

from favorit.funding.models import Product
from favorit.funding.schemas import CreateFundingRequestBody
from favorit.funding.services import FundingCreator


class TestFundingCreator:
    @pytest.mark.django_db
    def test_funding_creator_on_success(self):
        valid_request_body = {
            "name": "윤권이의 생일선물은 아이패드로 부탁해",
            "contents": "궈니는 아이패드가 참 좋더라",
            "due_date": "2022-09-03",
            "product": {
                "link": "https://www.apple.com/kr/shop/buy-ipad/ipad-air",
                "option": "WIFI에 색상은 금색 256GB",
                "price": 779000,
            },
            "recipient_name": "신윤권",
        }
        request_body = CreateFundingRequestBody(**valid_request_body)
        funding_creator = FundingCreator(request_body=request_body)
        assert funding_creator.create().id == 1
        assert Product.objects.count() == 1
