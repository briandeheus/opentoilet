from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("api.urls"), name="api"),
    path("admin/", admin.site.urls),
]
