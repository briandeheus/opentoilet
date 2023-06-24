from rest_framework import serializers

from restrooms.models import Amenity


class ReadAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]


class CreateAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["name"]
