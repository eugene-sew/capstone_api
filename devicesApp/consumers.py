import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import DatabaseError
from channels.db import database_sync_to_async
from .models import Device
from .serializers import DeviceSerializer

class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "device_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "device_updates",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        device_id = data.get('device_id')
        status = data.get('status')

        # Use database_sync_to_async for database operations
        try:
            await self.update_device_status(device_id, status)
            
            # Send WebSocket message
            await self.channel_layer.group_send(
                "device_updates",
                {
                    'type': 'status_update',
                    'message': {
                        'device_id': device_id,
                        'status': status,
                    }
                }
            )
        except Device.DoesNotExist:
            await self.send(text_data=json.dumps({'error': 'Device not found'}))
        except DatabaseError as e:
            await self.send(text_data=json.dumps({'error': str(e)}))

    @database_sync_to_async
    def update_device_status(self, device_id, status):
        try:
            device = Device.objects.get(mac_address=device_id)
            device.status = status
            device.save()
        except Device.DoesNotExist:
            raise Device.DoesNotExist("Device not found")
