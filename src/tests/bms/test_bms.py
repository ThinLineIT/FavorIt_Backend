import pytest
from django.test.client import Client
from django.urls import reverse

client = Client()


def test_hello():
    print(reverse("ninja:hello_world"))
    response = client.get(path=reverse("ninja:hello_world"))
    result = response.json()
    assert result["hello"] == "hello"
    assert result["world"] == "world"


class TestCreateBook:
    @pytest.mark.django_db
    def test_create_book(self):
        valid_request_body = {"name": "my book"}

        response = client.post(
            path=reverse("ninja:create_book"), data=valid_request_body, content_type="application/json"
        )

        assert response.json()["name"] == "my book"
