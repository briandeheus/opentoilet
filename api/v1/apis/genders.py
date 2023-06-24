from rest_framework.response import Response

from api.base_api import BaseAPI
from restrooms.consts import GENDER_LIST


class GendersAPI(BaseAPI):
    REQUIRES_AUTH = True

    def list(self, request):
        return Response(GENDER_LIST)
