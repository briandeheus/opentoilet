from django.contrib import admin

from ratings.models import Rating, RestroomPicture


# Register your models here.
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    search_fields = ["restroom", "comment"]
    list_display = [
        "restroom",
        "actor",
        "cleanliness_rating",
        "amenities_rating",
        "accessibility_rating",
        "created_on",
        "approved",
    ]
    autocomplete_fields = ["restroom", "actor"]


@admin.register(RestroomPicture)
class RestroomPictureAdmin(admin.ModelAdmin):
    search_fields = ["restroom"]
    list_display = ["restroom", "media"]
    autocomplete_fields = ["restroom", "actor"]
