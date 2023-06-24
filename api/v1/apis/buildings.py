from rest_framework import status
from rest_framework.response import Response

from api.base_api import BaseAPI
from api.v1.serializers.buildings import (
    CreateBuildingSerializer,
    ReadBuildingSerializer,
)
from buildings.models import Building


class BuildingsAPI(BaseAPI):
    REQUIRES_AUTH = True
    MODEL = Building
    READ_SERIALIZER = ReadBuildingSerializer

    def list(self, request):
        return self._list(request=request)

    def create(self, request):
        return self._create(request=request)

    def retrieve(self, request, pk):
        return self._retrieve(request=request, pk=pk)
