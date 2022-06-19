from favorit.debug.schemas import DebugLoginRequest
from favorit.favorit_user.models import FavorItUser
from favorit.favorit_user.services import AuthTokenPublisher


def debug_handle_login(request_body: DebugLoginRequest):
    favorit_user, _ = FavorItUser.objects.get_or_create(kakao_user_id=request_body.kakao_user_id)

    auth_token_publisher = AuthTokenPublisher(favorit_user=favorit_user)
    access_token, refresh_token = auth_token_publisher.publish()

    return {"access_token": access_token, "refresh_token": refresh_token}
