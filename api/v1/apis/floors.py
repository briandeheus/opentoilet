from rest_framework import status
from rest_framework.response import Response

from api.base_api import BaseAPI
from api.v1.serializers.amenities import CreateAmenitySerializer, ReadAmenitySerializer
from api.v1.serializers.buildings import (
    CreateBuildingSerializer,
    ReadBuildingSerializer,
)
from api.v1.serializers.floors import ReadFloorSerializer, CreateFloorSerializer
from buildings.models import Floor

import django_filters


class FloorFilter(django_filters.FilterSet):
    building = django_filters.CharFilter(field_name='building_id')
    floor_number = django_filters.NumberFilter()

    class Meta:
        model = Floor
        fields = ['building', 'floor_number']


class FloorsAPI(BaseAPI):
    REQUIRES_AUTH = True
    MODEL = Floor
    READ_SERIALIZER = ReadFloorSerializer
    CREATE_SERIALIZER = CreateFloorSerializer
    FILTER = FloorFilter

    def retrieve(self, request, pk):
        return self._retrieve(request=request, pk=pk)

    def list(self, request):
        return self._list(request=request)

    def create(self, request):
        return self._create(request=request)

    def update(self, request, pk):
        return self._update(request=request, pk=pk)
