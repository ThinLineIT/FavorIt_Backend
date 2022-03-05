from django.db import models


class BookType(models.TextChoices):
    NEW_BOOK = "NEW_BOOK", "새 책"
    USED_BOOK = "USED_BOOK", "중고 책"
    E_BOOK = "E_BOOKS", "E-Book"
