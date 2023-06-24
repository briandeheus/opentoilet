from django.db import models

from opentoilet.models import BaseModel


# Create your models here.
class APIKey(BaseModel):
    access_id = models.CharField(max_length=128)
