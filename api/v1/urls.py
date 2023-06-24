from django.urls import include, path
from rest_framework import routers

from api.v1.apis import account, amenities, buildings, floors, genders, restrooms, toilet_types

api_router = routers.DefaultRouter()
api_router.register(r"account", account.AccountAPI, basename="accounts")
api_router.register(r"amenities", amenities.AmenitiesAPI, basename="amenities")
api_router.register(r"buildings", buildings.BuildingsAPI, basename="buildings")
api_router.register(r"floors", floors.FloorsAPI, basename="floors")
api_router.register(r"genders", genders.GendersAPI, basename="genders")
api_router.register(r"restrooms", restrooms.RestroomsAPI, basename="restrooms")
api_router.register(r"toilet-types", toilet_types.ToiletTypesAPI, basename="toilet-types")

urlpatterns = [
    path("", include(api_router.urls)),
]
