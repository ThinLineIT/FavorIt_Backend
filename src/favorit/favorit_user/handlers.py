from ninja_jwt.tokens import RefreshToken

from favorit.favorit_user.models import FavorItUser
from favorit.favorit_user.schemas import LoginRequest
from favorit.integration.kakao.user_info_fetcher import KakaoUserInfoFetcher


def handle_login(request_body: LoginRequest) -> dict[str, str]:
    kakao_user_info_fetcher = KakaoUserInfoFetcher()
    kakao_user_info = kakao_user_info_fetcher.fetch(token=request_body.kakao_token)

    favorit_user, _ = FavorItUser.objects.get_or_create(kakao_user_id=kakao_user_info.id)

    refresh = RefreshToken.for_user(favorit_user)
    return {"access_token": str(refresh.access_token)}
