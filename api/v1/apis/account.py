from django.contrib.auth import authenticate
from rest_framework import decorators
from rest_framework.response import Response

from api.base_api import BaseAPI
from api.methods import encode_jwt, generate_api_key
from api.v1.serializers.account import (
    AccountSerializer,
    LoginRequestSerializer,
    LoginResponseSerializer,
)
from opentoilet.exceptions import APIAccessDenied


class AccountAPI(BaseAPI):
    REQUIRES_AUTH = False

    @decorators.action(
        methods=["POST"], detail=False, url_path="login", url_name="login"
    )
    def login(self, request):
        req_body = LoginRequestSerializer(data=request.data)
        req_body.is_valid(raise_exception=True)

        user = authenticate(
            username=req_body.validated_data["username"],
            password=req_body.validated_data["password"],
        )

        if not user:
            raise APIAccessDenied(
                code="invalid_credentials",
                message="The credentials you have provided are invalid",
            )

        if not user.account.setup_complete:
            raise APIAccessDenied(
                code="account_incomplete",
                message="This account has not been verified yet",
            )

        response = LoginResponseSerializer(
            data={"token": encode_jwt(api_key=generate_api_key(user=user))}
        )
        response.is_valid(raise_exception=True)
        return Response(response.data)

    def list(self, request):
        """
        Abusing the list api because a user should never get back more than one user.
        :param request:
        :return:
        """
        if request.user.is_anonymous:
            raise APIAccessDenied()

        return Response(AccountSerializer(instance=request.user).data)
