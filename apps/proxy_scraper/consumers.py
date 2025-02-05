# apps/proxy_scraper/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProxyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Connected to proxy updates'}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # For now, simply echo back the received message.
        await self.send(text_data=json.dumps({'message': text_data}))
