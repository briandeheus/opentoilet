from rest_framework import status
from rest_framework.response import Response

from api.base_api import BaseAPI
from api.v1.serializers.amenities import CreateAmenitySerializer, ReadAmenitySerializer
from api.v1.serializers.buildings import (
    CreateBuildingSerializer,
    ReadBuildingSerializer,
)
from restrooms.models import Amenity


class AmenitiesAPI(BaseAPI):
    REQUIRES_AUTH = True
    MODEL = Amenity
    READ_SERIALIZER = ReadAmenitySerializer
    CREATE_SERIALIZER = CreateAmenitySerializer

    def retrieve(self, request, pk):
        return self._retrieve(request=request, pk=pk)

    def list(self, request):
        return self._list(request=request)

    def create(self, request):
        return self._create(request=request)

    def update(self, request, pk):
        return self._update(request=request, pk=pk)
