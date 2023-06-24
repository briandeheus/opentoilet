from django.contrib.gis.geos import Point
from django.db.models import Sum
from rest_framework import serializers

from api.v1.serializers.amenities import ReadAmenitySerializer
from buildings.models import Building, Floor
from restrooms.models import RestroomToiletType, Restroom, ToiletType


class ReadRestroomSerializer(serializers.ModelSerializer):
    toilet_types = serializers.SerializerMethodField()
    toilet_count = serializers.SerializerMethodField()
    amenities = ReadAmenitySerializer(many=True)

    class Meta:
        model = Restroom
        fields = "__all__"

    def get_toilet_types(self, instance: Restroom):
        return [{"name": t.toilet_type.name, "count": t.count} for t in instance.restroomtoilettype_set.all()]

    def get_toilet_count(self, instance: Restroom):
        return RestroomToiletType.objects.filter(restroom=instance).aggregate(sum=Sum("count")).get("sum") or 0
