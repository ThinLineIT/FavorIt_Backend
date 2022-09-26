from django.db import models

from favorit.common.models import CommonTimestamp


class FavorItUser(CommonTimestamp):
    kakao_user_id = models.CharField(max_length=50, help_text="카카오 유저 ID")
    friends = models.ManyToManyField("self", symmetrical=False)
