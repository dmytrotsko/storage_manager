from django.db import models
from indussystem.models import Villa, User


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=128)
    storage = models.ForeignKey(Villa, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f'{self.name} at {self.storage.name} (q: {self.quantity})'


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('CR', 'Creation'),
        ('TR', 'Transition'),
        ('DL', 'Deletion')
    ]

    date = models.DateTimeField(auto_now_add=True, blank=True)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='CR')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=128)
    price_per_item = models.FloatField()
    storage_from = models.ForeignKey(Villa, blank=True, null=True, on_delete=models.CASCADE, related_name='storage_from')
    storage_to = models.ForeignKey(Villa, blank=True, null=True, on_delete=models.CASCADE, related_name='storage_to')
    quantity = models.IntegerField()

    def __str__(self):
        if self.type == 'TR':
            return f'Transition "{self.item_name}" from {self.storage_from} to {self.storage_to}'
        elif self.type == 'DL':
            return f'Deletion "{self.item_name}" from {self.storage_from}'
        else:
            return f'Creation "{self.item_name}" from {self.storage_from}'
