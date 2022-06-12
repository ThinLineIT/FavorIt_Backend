from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse

from favorit.funding.models import Funding

client = Client()


class TestCreateFunding:
    @pytest.mark.django_db
    def test_create_funding_on_success(self):
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
        response = client.post(
            path=reverse("favorit:create_funding"), data=valid_request_body, content_type="application/json"
        )
        data = response.json()
        assert data["message"] == ""
        assert Funding.objects.count() == 1
        assert data["data"]["funding_id"] == Funding.objects.all()[0].id
        assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.django_db
    def test_create_funding_on_fail_with_400(self):
        invalid_request_body = {
            "name": "윤권이의 생일선물은 아이패드로 부탁해",
            "contents": "궈니는 아이패드가 참 좋더라",
            "due_date": "2022-09-03",
            "product": {
                "link": "https://www.apple.com/kr/shop/buy-ipad/ipad-air",
                "option": "WIFI에 색상은 금색 256GB",
                "price": "abcde",  # price 값 타입이 다름
            },
            "recipient_name": "신윤권",
        }
        response = client.post(
            path=reverse("favorit:create_funding"), data=invalid_request_body, content_type="application/json"
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
