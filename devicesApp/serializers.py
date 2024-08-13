from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['mac_address', 'datetime_activated', 'latitude', 'longitude', 'reserve_name', 'status']
