from django.contrib.gis.geos import Point
from rest_framework.test import APIClient, APITestCase

from api.methods import create_account, encode_jwt, generate_api_key
from buildings.models import Building


class BaseTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.authed_client = APIClient()
        self.username = "testuser@gmail.com"
        self.password = "testpass"
        self.user = create_account(username=self.username, password=self.password)
        self.user.account.setup_complete = True
        self.user.account.save()
        self.authed_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {encode_jwt(api_key=generate_api_key(user=self.user))}"
        )

    def _create_buildings(self):
        return [
            Building.objects.create(name="Building 1", latlng=Point(37.7749, 122.4194)),
            Building.objects.create(name="Building 2", latlng=Point(37.7749, 122.4194)),
            Building.objects.create(name="Building 3", latlng=Point(37.7749, 122.4194)),
        ]
