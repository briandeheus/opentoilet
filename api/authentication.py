from rest_framework import authentication

from api.methods import get_user_from_bearer


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if not request.META.get("HTTP_AUTHORIZATION"):
            return None

        user = get_user_from_bearer(request.META.get("HTTP_AUTHORIZATION"))
        return user, None
