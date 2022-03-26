from django.db import models


class TextChoicesMixin:
    @classmethod
    def as_options(cls):
        return [{"text": type_.label, "value": type_.name} for type_ in BookType]  # type: ignore[attr-defined]


class BookType(TextChoicesMixin, models.TextChoices):
    NEW_BOOK = "NEW_BOOK", "새 책"
    USED_BOOK = "USED_BOOK", "중고 책"
    E_BOOK = "E_BOOKS", "E-Book"
