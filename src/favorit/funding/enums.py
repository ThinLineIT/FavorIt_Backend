from django.conf import settings
from django.db import models


class FundingState(models.TextChoices):
    OPENED = "OPENED", "펀딩 오픈"
    CLOSED = "CLOSED", "펀딩 닫힘"
    EXPIRED = "EXPIRED", "펀딩 만료"
    COMPLETED = "COMPLETED", "펀딩 완료"

    @classmethod
    def enable_closed_state(cls):
        return {cls.OPENED, cls.EXPIRED}


class BankEnum(models.TextChoices):
    NH = "NH", "NH농협"
    KB = "KB", "KB 국민"
    KAKAO = "KAKAO", "카카오뱅크"
    SHINHAN = "SHINHAN", "신한"
    WOORI = "WOORI", "우리"

    @classmethod
    def option_list(cls):
        result = []
        for bank in cls:  # type: ignore[attr-defined]
            element = {}
            element["text"] = bank.label
            element["value"] = bank.value
            element["image"] = f"https://{settings.S3_BUCKET}.{settings.S3_BASE_URL}/bank/{bank.value.lower()}.jpg"
            result.append(element)
        return result


class FundingImageType(models.TextChoices):
    PRESENT = "PRESENT", "선물하기 이미지"
    FUNDING_CREATE = "FUNDING_CREATE", "펀딩생성 이미지"