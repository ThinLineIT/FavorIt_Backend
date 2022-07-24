from datetime import datetime

from django.conf import settings
from django.db import models

from favorit.common.models import CommonTimestamp
from favorit.funding.enums import BankEnum, FundingState


class Funding(CommonTimestamp):
    maker = models.ForeignKey("FavorItUser", on_delete=models.DO_NOTHING, help_text="펀딩 생성자")
    product = models.ForeignKey("Product", on_delete=models.DO_NOTHING, help_text="제품 ID")
    name = models.CharField(max_length=200, help_text="펀딩 이름")
    contents = models.TextField(help_text="펀딩 내용")
    due_date = models.DateField(help_text="펀딩 만료 기한")
    state = models.CharField(
        max_length=100, choices=FundingState.choices, default=FundingState.OPENED, help_text="펀딩 상태"
    )

    @property
    def enable_closed(self) -> bool:
        return self.state in FundingState.enable_closed_state()

    @property
    def creation_date_format(self) -> str:
        return datetime.strftime(self.created_at, settings.DEFAULT_DATE_FORMAT)

    def progress_percent(self, total_amount) -> int:
        return int((total_amount / self.product.price) * 100)

    def change_state(self, state: FundingState):
        self.state = state
        self.save()


class FundingAmount(CommonTimestamp):
    funding = models.ForeignKey("Funding", on_delete=models.DO_NOTHING, help_text="펀딩 ID")
    amount = models.PositiveBigIntegerField(help_text="펀딩 모금 금액", default=0)

    def add_amount(self, amount):
        self.amount += amount
        self.save()


class Product(CommonTimestamp):
    link = models.CharField(max_length=500, help_text="제품 링크")
    price = models.IntegerField(help_text="제품 가격")
    option = models.TextField(help_text="제품 옵션")


class FundingPaymentResult(CommonTimestamp):
    funding = models.ForeignKey("Funding", on_delete=models.DO_NOTHING, help_text="펀딩 ID")
    full_name = models.CharField(max_length=20, help_text="정산 받는 사람 이름")
    bank_code = models.CharField(max_length=10, choices=BankEnum.choices, help_text="은행")
    account_number = models.CharField(max_length=30, help_text="계좌 번호")
    price = models.IntegerField(help_text="정산 받은 금액")
