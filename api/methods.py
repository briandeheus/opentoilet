import random
import string

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import Account
from api.models import APIKey


def generate_api_key(user):
    return APIKey.objects.create(actor=user)


def get_user(pk: str):
    access_key = APIKey.objects.get(pk=int(pk))
    return access_key.actor


def decode_jwt(token: str):
    data = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    return data.get("aid")


def encode_jwt(api_key: APIKey):
    return jwt.encode({"aid": api_key.pk}, key=settings.JWT_SECRET, algorithm="HS256")


def generate_otp(size=6, chars=None):
    if not chars:
        chars = string.ascii_letters + string.digits

    return "".join(random.choice(chars) for _ in range(size)).lower()


def clean_sensitive_data(data):
    if "password" in data:
        data["password"] = "****"

    if "private_key" in data:
        data["private_key"] = "****"

    return data


def create_account(username, password):
    user = User.objects.create_user(
        username=username, email=username, password=password
    )
    Account.objects.create(user=user)
    return user


def get_user_from_bearer(bearer=None):
    if not bearer:
        return None

    auth_header = bearer.split(" ")
    if len(auth_header) != 2:
        return None

    try:
        user = get_user(pk=decode_jwt(auth_header[1]))
    except Exception:
        raise AuthenticationFailed("Invalid credentials")
    if not user:
        raise AuthenticationFailed("Invalid credentials")

    return user
