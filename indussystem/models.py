from django.db import models


class Villa(models.Model):
    name = models.CharField(blank=False, max_length=100)

    class Meta:
        db_table = "Villa"
