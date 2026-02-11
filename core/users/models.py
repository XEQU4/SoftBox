from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    last_box_created = models.DateTimeField(null=True, blank=True)
    last_box_opened = models.DateTimeField(null=True, blank=True)
