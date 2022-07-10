from http import HTTPStatus

from ninja.errors import HttpError, ValidationError
from ninja.responses import Response
from ninja_extra import NinjaExtraAPI

from favorit.debug.api import debug_router
from favorit.favorit_user.api import auth_router
from favorit.funding.api import funding_router

api = NinjaExtraAPI(
    title="FavorIt API",
    version="1.0.0",
    description="FavorIt API 입니다.",
    urls_namespace="favorit",
)


@api.get(
    path="/health_check",
    url_name="health_check",
)
def health_check(request):
    return HTTPStatus.OK


@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return Response(data={"detail": exc.errors[0]["msg"], "message": ""}, status=HTTPStatus.BAD_REQUEST)


@api.exception_handler(HttpError)
def http_errors(request, exc):
    if exc.status_code == HTTPStatus.UNAUTHORIZED:
        return Response(data={"detail": str(exc), "message": ""}, status=HTTPStatus.UNAUTHORIZED)
    return Response(data={"detail": str(exc), "message": ""}, status=exc.status_code)


api.add_router("/debug", debug_router)
api.add_router("/auth", auth_router)
api.add_router("/", funding_router)
