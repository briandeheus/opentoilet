from rest_framework import serializers

from restrooms.models import ToiletType


class ReadToiletTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToiletType
        fields = "__all__"
