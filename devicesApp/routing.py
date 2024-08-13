from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/devices/', consumers.DeviceConsumer.as_asgi()),
]
