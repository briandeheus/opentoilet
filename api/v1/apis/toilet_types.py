from api.base_api import BaseAPI
from api.v1.serializers.amenities import ReadAmenitySerializer

from api.v1.serializers.toilet_types import ReadToiletTypeSerializer
from restrooms.models import Amenity, ToiletType


class ToiletTypesAPI(BaseAPI):
    REQUIRES_AUTH = True
    MODEL = ToiletType
    READ_SERIALIZER = ReadToiletTypeSerializer

    def retrieve(self, request, pk):
        return self._retrieve(request=request, pk=pk)

    def list(self, request):
        return self._list(request=request)
