import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ImportLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.playlist_id = self.scope['url_route']['kwargs']['playlist_id']
        self.group_name = f'import_logs_{self.playlist_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_log_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))