from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse

from favorit.funding.enums import FundingState
from tests.favorit.funding.test_mixins import TestFundingMixins

client = Client()


class TestCloseFundingAcceptance(TestFundingMixins):
    def _call_api(self, funding, jwt_access_token):
        response = client.post(
            path=reverse("favorit:close_funding", kwargs={"funding_id": funding.id}),
            content_type="application/json",
            **{"HTTP_Authorization": f"Bearer {jwt_access_token}"},
        )
        return response

    @pytest.mark.django_db
    def test_close_funding_on_success(self, jwt_access_token):
        _, _, funding = self.create_funding()

        response = self._call_api(funding, jwt_access_token)

        assert response.status_code == HTTPStatus.OK
        funding.refresh_from_db()
        assert funding.state == FundingState.CLOSED

    @pytest.mark.parametrize("not_enable_closed", [FundingState.CLOSED, FundingState.COMPLETED])
    @pytest.mark.django_db
    def test_close_funding_on_fail(self, jwt_access_token, not_enable_closed):
        _, _, funding = self.create_funding()

        funding.state = not_enable_closed
        funding.save()

        response = self._call_api(funding, jwt_access_token)

        assert response.status_code == HTTPStatus.BAD_REQUEST
