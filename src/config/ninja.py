from ninja import NinjaAPI

from bms.book.api import bms_options_router, bms_router

api = NinjaAPI(
    title="NinjaAPI",
    version="1.0.0",
    description="집에 있는 책을 관리하는 시스템 API 입니다",
    urls_namespace="bms",
)


api.add_router("/", bms_router)
api.add_router("/options/", bms_options_router)
