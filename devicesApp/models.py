from django.db import models

# Create your models here.

class Device(models.Model):
    mac_address = models.CharField(max_length=17, unique=True,primary_key=True)
    datetime_activated = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    reserve_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default='offline')

    def __str__(self):
        return f"{self.mac_address} - {self.reserve_name}"
