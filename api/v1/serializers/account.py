from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id"]


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
