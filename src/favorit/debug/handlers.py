from ninja_jwt.tokens import RefreshToken

from favorit.debug.schemas import DebugLoginRequest
from favorit.favorit_user.models import FavorItUser


def debug_handle_login(request_body: DebugLoginRequest):
    favorit_user, _ = FavorItUser.objects.get_or_create(kakao_user_id=request_body.user_id)

    refresh = RefreshToken.for_user(favorit_user)
    return {"access_token": str(refresh.access_token)}
