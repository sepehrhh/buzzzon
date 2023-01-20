from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from . import models
from rest_framework.authtoken.models import Token


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('in fuuuuuuuuuuuuuuuuuunc connect')

        # get receiver username
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        # get sender username
        user_token = self.scope['cookies']['userToken']
        token = Token.objects.get(key=user_token)
        self.sender = token.user_id
        self.room_group_name = 'chat_{}_with_{}'.format(min(self.sender, self.user_id), max(self.sender, self.user_id))

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        print('in fuuuuuuuuuuuuuuuuuunc disconnect')

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print('in fuuuuuuuuuuuuuuuuuunc receive', text_data)

        # convert received data to dict and get the data
        json_data = json.loads(text_data)
        message = json_data.get('message')

        # save received message to db
        message_obj = models.Message.objects.create(
            sender=models.User.objects.get(id=self.sender),
            receiver=models.User.objects.get(id=self.user_id),
            message=message
        )

        message_to_return = {
            'message': message,
            'sender': self.sender,
            'time_sent': message_obj.created.strftime('%m/%d/%Y %H:%M:%S')
        }
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_to_return
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        print('in fuuuuuuuuuuuuuuuuuunc chat_message')

        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
