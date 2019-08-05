from django.db import models
from indussystem.models import Villa


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=128)
    storage = models.ForeignKey(Villa, on_delete=models.CASCADE)
    quantity = models.IntegerField()
