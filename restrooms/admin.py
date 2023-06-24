from django.contrib import admin

from restrooms.models import Amenity, Restroom, RestroomToiletType, ToiletType


# Register your models here.
@admin.register(ToiletType)
class ToiletTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


@admin.register(Amenity)
class AmenitiesAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


@admin.register(Restroom)
class RestroomAdmin(admin.ModelAdmin):
    search_fields = ["building__name", "floor__floor_number", "gender"]
    list_display = ["building", "floor", "gender"]
    autocomplete_fields = ["building", "floor", "toilet_types", "amenities"]


@admin.register(RestroomToiletType)
class RestroomToiletTypeAdmin(admin.ModelAdmin):
    search_fields = ["restroom", "toilet_type__name"]
    list_display = ["restroom", "toilet_type", "count"]
    autocomplete_fields = ["restroom", "toilet_type"]
