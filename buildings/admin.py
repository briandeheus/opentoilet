from django.contrib import admin

from buildings.models import Building, Floor


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "latlng"]


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    search_fields = ["building__name", "floor_number"]
    list_display = ["building", "floor_number"]
    autocomplete_fields = ["building"]
