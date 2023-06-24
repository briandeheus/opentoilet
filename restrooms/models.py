from django.db import models

from opentoilet.models import BaseModel
from restrooms.consts import GENDER_CHOICES


class Restroom(BaseModel):
    building = models.ForeignKey("buildings.Building", on_delete=models.CASCADE)
    floor = models.ForeignKey("buildings.Floor", on_delete=models.CASCADE)
    toilet_types = models.ManyToManyField(
        "restrooms.ToiletType", through="RestroomToiletType"
    )
    amenities = models.ManyToManyField("restrooms.Amenity")
    gender = models.CharField(max_length=32, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.building.name} - floor {self.floor.floor_number} - {self.gender}"


class RestroomToiletType(BaseModel):
    restroom = models.ForeignKey(Restroom, on_delete=models.CASCADE)
    toilet_type = models.ForeignKey("restrooms.ToiletType", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.restroom} - {self.toilet_type.name} - {self.count}"


class ToiletType(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Amenity(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
