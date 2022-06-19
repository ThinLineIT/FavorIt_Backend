from typing import Tuple

from ninja_jwt.tokens import RefreshToken


class AuthTokenPublisher:
    def __init__(self, favorit_user):
        self.favorit_user = favorit_user

    def publish(self) -> Tuple[str, str]:
        refresh = RefreshToken.for_user(self.favorit_user)
        return str(refresh.access_token), str(refresh)
