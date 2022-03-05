from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from bms.enums import BookType
from bms.models import Author, Book

client = Client()


def test_hello():
    response = client.get(path=reverse("ninja:hello_world"))
    result = response.json()
    assert result["hello"] == "hello"
    assert result["world"] == "world"


class TestCreateBook:
    @pytest.mark.django_db
    def test_create_book(self):

        author = Author.objects.create(name="Kent Beck")
        valid_request_body = {
            "author_id": author.id,
            "name": "my book",
            "sub_name": "no sub name",
            "type": BookType.NEW_BOOK,
            "description": "재미있는 책 입니다",
            "published_at": timezone.localdate(),
            "price": 13000,
            "sale_price": 10000,
            "purchased_at": timezone.localdate(),
        }

        response = client.post(
            path=reverse("ninja:create_book"), data=valid_request_body, content_type="application/json"
        )

        assert response.status_code == HTTPStatus.CREATED
        assert Book.objects.count() == 1
        book = Book.objects.all()[0]
        assert book.author.id == valid_request_body["author_id"]
        assert book.name == valid_request_body["name"]
