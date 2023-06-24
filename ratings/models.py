from django.db import models

from opentoilet.models import BaseModel


class Rating(BaseModel):
    restroom = models.ForeignKey("restrooms.Restroom", on_delete=models.CASCADE)
    cleanliness_rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    amenities_rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    accessibility_rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    comment = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.actor} - {self.restroom}"


class RestroomPicture(BaseModel):
    restroom = models.ForeignKey("restrooms.Restroom", on_delete=models.CASCADE)
    media = models.ForeignKey("media.Media", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.restroom} - Picture"
