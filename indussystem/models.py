from django.db import models
from django.contrib.auth.models import AbstractUser


class Villa(models.Model):
    name = models.CharField(blank=False, max_length=100)

    class Meta:
        db_table = "Villa"

    def __str__(self):
        return self.name


class User(AbstractUser):

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'User'
