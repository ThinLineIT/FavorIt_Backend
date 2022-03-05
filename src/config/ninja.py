from ninja import NinjaAPI

from bms.views import bms_router

api = NinjaAPI()


api.add_router("/", bms_router)
