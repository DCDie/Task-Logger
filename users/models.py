from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    username = models.EmailField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_superuser = False,
    is_staff = False
