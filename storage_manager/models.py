from django.db import models
from indussystem.models import Villa


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=128)
    storage = models.ForeignKey(Villa, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.name} at {self.storage.name} (q: {self.quantity})'

