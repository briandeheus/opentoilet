from django.contrib.gis.geos import Point
from django.db.models import Sum
from rest_framework import serializers

from buildings.models import Building
from restrooms.models import RestroomToiletType


class ReadBuildingSerializer(serializers.ModelSerializer):
    latlng = serializers.SerializerMethodField()
    toilet_count = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = "__all__"
        read_only_fields = ["id", "name", "latlng", "toilet_count"]

    def get_latlng(self, instance: Building):
        return [instance.latlng[0], instance.latlng[1]]

    def get_toilet_count(self, instance: Building):
        toilet_count = (
            RestroomToiletType.objects.filter(restroom__building=instance)
            .aggregate(sum=Sum("count"))
            .get("sum")
        )

        if toilet_count is None:
            return 0
        return toilet_count


class CreateBuildingSerializer(serializers.ModelSerializer):
    latlng = serializers.ListField(
        max_length=2, min_length=2, child=serializers.FloatField()
    )

    class Meta:
        model = Building
        fields = ["name", "latlng"]

    def validate_latlng(self, value):
        return Point(*value)
