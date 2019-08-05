import datetime
from django.db import models
from indussystem.models import Villa


class ServiceType(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    class Meta:
        db_table = 'Service_type'

    def __str__(self):
        return self.name


class Service(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    villa = models.ForeignKey(Villa, related_name='service_villa', null=True, blank=True, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    type = models.ForeignKey(ServiceType, related_name='type', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Service'

    def __str__(self):
        template = 'Type: {}.type for villa: {}.storage.storage_name'
        return template.format(self)


class VillaReports(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    villa = models.ForeignKey(Villa, related_name='villa', null=True, blank=True, on_delete=models.CASCADE)
    income = models.FloatField(default=0)
    expenses = models.FloatField(default=0)
    occupancy = models.IntegerField(default=0)
    profit = models.FloatField(default=0)
    averange_price = models.FloatField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'VillaReport'

    def __str__(self):
        return self.villa.name

    def __float__(self):
        return self.income, self.expenses, self.occupancy
