from django.db import models

from bms.book.enums import BookType


class BookQuerySet(models.QuerySet):
    def new_book(self):
        return self.filter(type=BookType.NEW_BOOK)

    def used_book(self):
        return self.filter(type=BookType.USED_BOOK)

    def e_book(self):
        return self.filter(type=BookType.E_BOOK)
