from datetime import date, datetime

from django.conf import settings

from favorit.funding.enums import FundingState
from favorit.funding.models import Funding


def run():
    today = date.today()
    to_expire_fundings = Funding.objects.filter(state=FundingState.OPENED, due_date__lt=today)
    to_expire_fundings.update(state=FundingState.EXPIRED, updated_at=datetime.now())

    today_format = datetime.strftime(today, settings.DEFAULT_DATE_FORMAT)

    # TODO: 추후에 메일과 슬랙으로 메세지 보내도록 설정
    print(f"{today_format} 의 만료된 펀딩의 개수는 {to_expire_fundings.count()} 개 입니다")
