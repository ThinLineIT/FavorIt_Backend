from django.db import models

from bms.book.enums import BookType
from bms.book.querysets import BookQuerySet
from bms.common.models import CommonTimestamp


class Author(CommonTimestamp):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(CommonTimestamp):
    author = models.ForeignKey("Author", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    sub_name = models.CharField(max_length=300, default="")
    type = models.CharField(max_length=30, choices=BookType.choices, default=BookType.NEW_BOOK)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    sale_price = models.DecimalField(max_digits=5, decimal_places=0, null=True)
    tags = models.ManyToManyField("Tag")
    purchased_at = models.DateField(null=True)
    published_at = models.DateField(null=True)

    objects = BookQuerySet.as_manager()

    def __str__(self):
        return self.name


class Tag(CommonTimestamp):
    name = models.CharField(max_length=100)
