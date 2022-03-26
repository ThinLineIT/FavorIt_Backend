from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from bms.book.enums import BookType
from bms.book.models import Author, Book

client = Client()


class TestCreateBook:
    @pytest.mark.django_db(transaction=True)
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

        response = client.post(path=reverse("ninja:books"), data=valid_request_body, content_type="application/json")

        assert response.status_code == HTTPStatus.CREATED
        assert Book.objects.count() == 1
        book = Book.objects.all()[0]
        assert book.author.id == valid_request_body["author_id"]
        assert book.name == valid_request_body["name"]


class TestRetrieveBooks:
    @pytest.mark.django_db(transaction=True)
    def test_retrieve_books(self):
        author = Author.objects.create(name="Kent Beck")
        book = Book.objects.create(
            **{
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
        )

        response = client.get(path=reverse("ninja:books"), content_type="application/json")

        assert response.status_code == HTTPStatus.OK
        result = response.json()
        assert len(result) == 1
        book.refresh_from_db()
        assert result[0]["author"] == book.author.name
        assert result[0]["name"] == book.name
        assert result[0]["sub_name"] == book.sub_name


class TestBookTypesOptionList:
    def test_retrieve_book_types_option_list(self):
        response = client.get(path=reverse("ninja:book_types_option_list"), content_type="application/json")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == [
            {"text": "새 책", "value": "NEW_BOOK"},
            {"text": "중고 책", "value": "USED_BOOK"},
            {"text": "E-Book", "value": "E_BOOK"},
        ]
