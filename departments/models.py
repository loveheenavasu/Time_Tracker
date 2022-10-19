from django.conf.global_settings import AUTH_USER_MODEL
from django.conf import settings
from django.db import models


# Create your models here.
class Departments(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
