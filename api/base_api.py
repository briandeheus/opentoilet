import logging
import traceback

from django.utils.timezone import now
from rest_framework import response, status, viewsets
from rest_framework.response import Response

from api import authentication
from api.methods import clean_sensitive_data
from opentoilet import exceptions
from opentoilet.exceptions import APINotFound

log = logging.getLogger(__name__)


class BaseAPI(viewsets.GenericViewSet):
    authentication_classes = [authentication.JWTAuthentication]
    REQUIRES_AUTH = False
    ENTITLEMENTS = set()
    MODEL = None
    READ_SERIALIZER = None
    CREATE_SERIALIZER = None
    FILTER = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if self.REQUIRES_AUTH:
            self._check_auth(request=request)

        if self.REQUIRES_AUTH and self.ENTITLEMENTS:
            self._check_entitlements(request=request)

    def _check_auth(self, request):
        if request.user.is_anonymous:
            raise exceptions.APIAccessDenied(
                "no_auth", "Missing authentication credentials"
            )

        # Store last activity for authenticated user
        if request.user.is_authenticated:
            request.user.account.last_activity = now()
            request.user.account.save()

    def _check_entitlements(self, request):
        if not self.ENTITLEMENTS.issubset(set(request.user.account.entitlements)):
            raise exceptions.APIAccessDenied(
                "missing_entitlements", f"Missing entitlements: {self.ENTITLEMENTS}"
            )

    def handle_exception(self, exc):
        tb = traceback.TracebackException.from_exception(exc)
        get_data = dict(self.request.GET)
        data = self.request.data
        post_data = []

        # Clean clean clean. Don't want to log this.
        # Also checking whether it's bulk insert or not
        if isinstance(data, list):
            for d in data:
                raw_post_data = dict(d)
                post_data.append(clean_sensitive_data(raw_post_data))
        else:
            raw_post_data = dict(self.request.data)
            post_data = clean_sensitive_data(raw_post_data)

        get_data = clean_sensitive_data(get_data)

        logging.error(
            "Exception=%s api=%s method=%s user=%s data=%s path=%s query=%s",
            "".join(tb.format()),
            self.get_view_name(),
            self.request.method,
            self.request.user.username,
            post_data,
            self.request.path,
            get_data,
        )

        try:
            return super().handle_exception(exc)
        except exceptions.APINotFound as e:
            return response.Response({"error": e.message, "code": e.code}, status=404)
        except (exceptions.APIException, exceptions.APIAccessDenied) as e:
            return response.Response({"error": e.message, "code": e.code}, status=400)
        except Exception:
            return response.Response(
                {"error": "Something went wrong.", "code": "unknown"}, status=500
            )

    def get_queryset(self):
        return self.MODEL.objects.all()

    def _get_instance(self, many=False, **kwargs):
        qs = self.MODEL.objects.get
        if many is True:
            qs = self.MODEL.objects.filter

        try:
            return qs(**kwargs)
        except self.MODEL.DoesNotExist:
            raise APINotFound()

    def _retrieve(self, request, pk):
        try:
            return Response(
                self.READ_SERIALIZER(instance=self._get_instance(pk=pk)).data,
                status=status.HTTP_200_OK,
            )
        except self.MODEL.DoesNotExist:
            raise APINotFound()

    def _list(self, request, **kwargs):
        if self.FILTER:
            f = self.FILTER(request.GET, queryset=self.get_queryset())
            qs = f.qs
        else:
            qs = self.MODEL.objects.filter(**kwargs)
        return self.get_paginated_response(
            self.READ_SERIALIZER(
                self.paginate_queryset(qs),
                many=True,
            ).data
        )

    def _create(self, request):
        serializer = self.CREATE_SERIALIZER(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.actor = request.user
        instance.save()

        return Response(
            self.READ_SERIALIZER(instance=instance).data,
            status=status.HTTP_201_CREATED,
        )

    def _update(self, request, pk):
        instance = self._get_instance(pk=pk)
        serializer = self.CREATE_SERIALIZER(
            data=request.data, instance=instance, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            self.READ_SERIALIZER(instance=instance).data,
            status=status.HTTP_200_OK,
        )
