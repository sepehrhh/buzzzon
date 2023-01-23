from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import utils


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope['user'] is AnonymousUser:
            return await self.close()
        else:
            await self.accept()
        self.contact_id = self.scope['url_route']['kwargs']['contact_id']
        chat_users_min_id = min(self.scope['user'].id, self.contact_id)
        chat_users_max_id = max(self.scope['user'].id, self.contact_id)
        self.chat_name = f'user_{chat_users_min_id}_to_{chat_users_max_id}_chat'
        await self.channel_layer.group_add(
            self.chat_name,
            self.channel_name,
        )

    async def disconnect(self, code):
        try:
            if self.scope['user'] is AnonymousUser:
                return

            # Leave room group
            await self.channel_layer.group_discard(
                self.chat_name,
                self.channel_name
            )
        except:
            pass

    async def receive_json(self, content, **kwargs):
        message = await utils.create_chat_message(
            sender=self.scope['user'],
            receiver_id=self.contact_id,
            message=content
        )

        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'chat_message',
                'message': {
                    'text': message.content,
                    'sender': self.scope['user'].email,
                    'time_sent': message.created.strftime('%m/%d/%Y %H:%M:%S'),
                    'type': message.type,
                }
            }
        )

    async def chat_message(self, event):
        """
        chat_message message type handler
        :param event:
        :return:
        """
        message = event['message']
        # Send message to WebSocket
        await self.send_json({
            'message': message
        })
