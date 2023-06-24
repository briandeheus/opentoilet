from django.contrib.gis.geos import Point
from django.db.models import Sum
from rest_framework import serializers

from api.v1.serializers.restrooms import ReadRestroomSerializer
from buildings.models import Building, Floor
from restrooms.models import RestroomToiletType, Restroom, ToiletType


class ReadFloorSerializer(serializers.ModelSerializer):
    restrooms = serializers.SerializerMethodField()
    building = serializers.SerializerMethodField()

    class Meta:
        model = Floor
        fields = "__all__"

    def get_restrooms(self, instance: Floor):
        return ReadRestroomSerializer(many=True, instance=instance.restroom_set.all()).data

    def get_building(self, instance: Floor):
        return {
            "id": instance.building.id,
            "name": instance.building.name
        }


class CreateFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ["floor_number", "building"]
