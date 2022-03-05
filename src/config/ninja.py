from ninja import NinjaAPI

from bms.views import bms_router
from config.routers import bms_options_router

api = NinjaAPI(
    title="NinjaAPI",
    version="1.0.0",
    description="집에 있는 책을 관리하는 시스템 API 입니다",
    urls_namespace="bms",
)


api.add_router("/", bms_router)
api.add_router("/options/", bms_options_router)
