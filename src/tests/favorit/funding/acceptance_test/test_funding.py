from http import HTTPStatus

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse

from favorit.favorit_user.models import FavorItUser
from favorit.funding.models import Funding, Product

client = Client()


class TestCreateFunding:
    @pytest.mark.django_db
    def test_create_funding_on_success(self, jwt_access_token):
        valid_request_body = {
            "name": "윤권이의 생일선물은 아이패드로 부탁해",
            "contents": "궈니는 아이패드가 참 좋더라",
            "due_date": "2022-09-03",
            "product": {
                "link": "https://www.apple.com/kr/shop/buy-ipad/ipad-air",
                "option": "WIFI에 색상은 금색 256GB",
                "price": 779000,
            },
        }
        response = client.post(
            path=reverse("favorit:create_funding"),
            data=valid_request_body,
            content_type="application/json",
            **{"HTTP_Authorization": f"Bearer {jwt_access_token}"},
        )
        data = response.json()
        assert data["message"] == ""
        assert Funding.objects.count() == 1
        funding = Funding.objects.all()[0]
        assert data["data"]["funding_id"] == funding.id
        assert data["data"]["link_for_sharing"] == f"{settings.BASE_URL}/funding/{funding.id}"
        assert response.status_code == HTTPStatus.CREATED


class TestRetrieveFunding:
    @pytest.mark.django_db
    def test_retrieve_funding_on_success(self, jwt_access_token):
        product = Product.objects.create(link="testlink", price=1000, option="some options")
        maker = FavorItUser.objects.create(kakao_user_id="12345")
        funding = Funding.objects.create(
            maker=maker, product=product, name="some funding", contents="some contents", due_date="2022-01-01"
        )
        response = client.get(
            path=reverse("favorit:retrieve_funding_detail", kwargs={"funding_id": funding.id}),
            content_type="application/json",
            **{"HTTP_Authorization": f"Bearer {jwt_access_token}"},
        )
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["message"] == ""
        assert data["data"]["name"] == funding.name
        assert data["data"]["contents"] == funding.contents
        assert data["data"]["due_date"] == funding.due_date
        assert data["data"]["progress_percent"] == 0
        assert data["data"]["link_for_sharing"] == f"https://www.favorit.com/funding/{funding.id}"
        assert data["data"]["product"]["link"] == product.link
        assert data["data"]["product"]["option"] == product.option
        assert data["data"]["product"]["price"] == product.price

    @pytest.mark.django_db
    def test_retrieve_funding_on_fail(self, jwt_access_token):
        response = client.get(
            path=reverse("favorit:retrieve_funding_detail", kwargs={"funding_id": 111223}),
            content_type="application/json",
            **{"HTTP_Authorization": f"Bearer {jwt_access_token}"},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
