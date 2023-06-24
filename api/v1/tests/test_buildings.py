from django.urls import reverse
from rest_framework import status

from api.v1.serializers.buildings import ReadBuildingSerializer
from buildings.models import Building
from opentoilet.tests import BaseTest


class BuildingsTestCase(BaseTest):
    base_url = reverse("buildings-list")

    def test_list(self):
        self._create_buildings()
        response = self.authed_client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)

    def test_create(self):
        data = {"name": "Test Building", "latlng": [123.45, 67.89]}
        response = self.authed_client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            ReadBuildingSerializer(
                instance=Building.objects.get(id=response.data["id"])
            ).data,
        )

        print(response.data)

        response = self.authed_client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_create_building_missing_name(self):
        data = {"latlng": [123.45, 67.89]}
        response = self.authed_client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
