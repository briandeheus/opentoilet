from bson import objectid
from django.db import models


def make_object_id():
    return str(objectid.ObjectId())


class BaseModel(models.Model):
    actor = models.ForeignKey(
        "auth.User", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-id"]
