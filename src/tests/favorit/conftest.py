import pytest
from ninja_jwt.tokens import RefreshToken

from favorit.favorit_user.models import FavorItUser


@pytest.fixture()
def favorit_user():
    return FavorItUser.objects.create(kakao_user_id=1)


@pytest.fixture
def jwt_access_token(favorit_user):
    refresh = RefreshToken.for_user(favorit_user)
    return str(refresh.access_token)
