from django.contrib import admin

from media.models import Media


class MediaAdmin(admin.ModelAdmin):
    list_display = ["id", "file_name", "file_type", "actor", "created_on", "updated_on"]
    list_filter = ["file_type", "actor"]
    search_fields = ["file_name"]
    readonly_fields = ["thumbnail", "file_size"]
    autocomplete_fields = ["actor"]


admin.site.register(Media, MediaAdmin)
