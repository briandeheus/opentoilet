from django.contrib import admin

from api.models import APIKey


class APIKeyAdmin(admin.ModelAdmin):
    list_display = ["id", "access_id", "actor", "created_on", "updated_on"]
    list_filter = ["actor"]
    search_fields = ["access_id"]


admin.site.register(APIKey, APIKeyAdmin)
