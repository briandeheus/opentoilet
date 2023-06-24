from django.db import models

from media.consts import ALL_MEDIA_ACCEPTED, MEDIA_METADATA_FIELDS, MEDIA_TYPE_CHOICES
from media.validators import FileMediaValidator
from opentoilet.models import BaseModel

MEDIA_VALIDATORS = [FileMediaValidator(content_types=ALL_MEDIA_ACCEPTED)]


# Create your models here.
class Media(BaseModel):
    file = models.FileField(
        null=True,
        blank=True,
        validators=MEDIA_VALIDATORS,
    )
    metadata = models.JSONField(default=dict)
    thumbnail = models.ImageField()
    file_name = models.CharField(max_length=600, null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=32, choices=MEDIA_TYPE_CHOICES)

    def __str__(self):
        return f"{self.file_name}"

    def set_metadata(self, key, value):
        if key not in MEDIA_METADATA_FIELDS:
            raise Exception(f"Key {key} not allowed in metadata")

        self.metadata[key] = value
