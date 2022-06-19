from typing import Tuple

from ninja_jwt.tokens import RefreshToken

from favorit.favorit_user.models import FavorItUser


def get_auth_tokens(kakao_user_id: int) -> Tuple[str, str]:
    favorit_user, _ = FavorItUser.objects.get_or_create(kakao_user_id=kakao_user_id)
    refresh = RefreshToken.for_user(favorit_user)
    return str(refresh.access_token), str(refresh)
