from django.db import models


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.DO_NOTHING)
    setup_complete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
