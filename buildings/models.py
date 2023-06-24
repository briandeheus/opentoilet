from django.contrib.gis.db.models import PointField
from django.db import models

from opentoilet.models import BaseModel


class Building(BaseModel):
    name = models.CharField(max_length=100)
    latlng = PointField()

    def __str__(self):
        return self.name


class Floor(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    floor_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.building.name} - Floor {self.floor_number}"

    class Meta:
        ordering = ["floor_number"]
