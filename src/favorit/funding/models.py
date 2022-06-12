from django.db import models

from favorit.common.models import CommonTimestamp


class Funding(CommonTimestamp):
    product_id = models.ForeignKey("Product", on_delete=models.DO_NOTHING, help_text="제품 ID")
    name = models.CharField(max_length=200, help_text="펀딩 이름")
    contents = models.TextField(help_text="펀딩 내용")
    due_date = models.DateField(help_text="펀딩 만료 기한")
    recipient_name = models.CharField(max_length=50, help_text="수취인 이름")


class Product(CommonTimestamp):
    link = models.CharField(max_length=500, help_text="제품 링크")
    price = models.IntegerField(help_text="제품 가격")
    options = models.ManyToManyField("Option", through="ProductOption", help_text="제품 옵션")


class Option(CommonTimestamp):
    name = models.CharField(max_length=100, help_text="제품 옵션 이름")


class ProductOption(CommonTimestamp):
    product_id = models.ForeignKey("Product", on_delete=models.DO_NOTHING, help_text="제품 ID")
    option_id = models.ForeignKey("Option", on_delete=models.DO_NOTHING, help_text="제품 옵션 ID")
