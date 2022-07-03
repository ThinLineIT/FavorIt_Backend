from django.db import models

from favorit.common.models import CommonTimestamp


class Funding(CommonTimestamp):
    product = models.ForeignKey("Product", on_delete=models.DO_NOTHING, help_text="제품 ID")
    name = models.CharField(max_length=200, help_text="펀딩 이름")
    contents = models.TextField(help_text="펀딩 내용")
    due_date = models.DateField(help_text="펀딩 만료 기한")


class FundingAmount(CommonTimestamp):
    funding = models.ForeignKey("Funding", on_delete=models.DO_NOTHING, help_text="펀딩 ID")
    amount = models.PositiveBigIntegerField(help_text="펀딩 모금 금액", default=0)

    def add_amount(self, amount):
        self.amount = amount
        self.save()


class Product(CommonTimestamp):
    link = models.CharField(max_length=500, help_text="제품 링크")
    price = models.IntegerField(help_text="제품 가격")
    option = models.TextField(help_text="제품 옵션")
