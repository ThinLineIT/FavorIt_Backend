from django.db import models


class FundingState(models.TextChoices):
    OPENED = "OPENED", "펀딩 오픈"
    CLOSED = "CLOSED", "펀딩 닫힘"
    EXPIRED = "EXPIRED", "펀딩 만료"
    COMPLETED = "COMPLETED", "펀딩 완료"

    @classmethod
    def enable_closed_state(cls):
        return {cls.OPENED, cls.EXPIRED}
