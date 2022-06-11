from ninja import NinjaAPI

from favorit.favorit_user.api import auth_router
from favorit.funding.api import funding_router

api = NinjaAPI(
    title="FavorIt API",
    version="1.0.0",
    description="FavorIt API 입니다.",
    urls_namespace="favorit",
)

api.add_router("/auth", auth_router)
api.add_router("/", funding_router)
