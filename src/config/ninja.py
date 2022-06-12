from http import HTTPStatus

from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.responses import Response

from favorit.favorit_user.api import auth_router
from favorit.funding.api import funding_router

api = NinjaAPI(
    title="FavorIt API",
    version="1.0.0",
    description="FavorIt API 입니다.",
    urls_namespace="favorit",
)


@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return Response(data=[], status=HTTPStatus.BAD_REQUEST)


# api.add_exception_handler(ValidationError, validation_error_handler)


api.add_router("/auth", auth_router)
api.add_router("/", funding_router)
