from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from user.models import User
from chatapp.models import PrivateChat, PrivateMessage
from urllib.parse import parse_qs
import json
from asgiref.sync import sync_to_async
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder


class DateTimeJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y/%m/%d %H:%M:%S')
        return super().default(obj)
    

class PrivateChatsConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        requested_user = self.scope['user']
        self.target_username = parse_qs(self.scope['query_string'].decode('utf8')).get('username', [None])[0]

        if requested_user.is_authenticated:
            self.private_chat = await self.user_private_chat(self.target_username, requested_user.username)
            # self.chat_id = private_chat[2]

            if self.private_chat:
                await self.channel_layer.group_add(
                    f"private_chat_{self.private_chat[0]}_{self.private_chat[1]}",
                    self.channel_name
                )
                await self.send({
                    'type': 'websocket.accept'
                })
            else:
                await self.send({
                    'type': 'websocket.close'
                })
        else:
            await self.send({
                'type': 'websocket.close'
            })
    
    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard(
            f'private_chat_{self.private_chat[0]}_{self.private_chat[1]}',
            self.channel_name
            )
        raise StopConsumer()

    async def websocket_receive(self, text_date=None, bytes_date=None):
        if text_date:
            text_loaded = json.loads(text_date['text'])
            message = text_loaded['text']
            print(datetime.now())
            await self.channel_layer.group_send(
                f'private_chat_{self.private_chat[0]}_{self.private_chat[1]}',
                {
                    'type': 'sendMessageGroup',
                    'message': json.dumps({'sender': self.scope['user'].username, 'receiver': self.target_username, 'text': message, 'date_time': datetime.now()}, cls=DateTimeJsonEncoder)
                }
            )
            await self.save_message_in_db(message)
    
    
    async def sendMessageGroup(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

            

    @database_sync_to_async
    def user_private_chat(self, target_username, requested_user):
        try:
            p = PrivateChat.objects.get(Q(user1__username=requested_user, user2__username=target_username) | Q(user1__username=target_username, user2__username=requested_user))
            return [p.user1.username, p.user2.username, p.pk]
        except PrivateChat.DoesNotExist:
            return None
    
    @database_sync_to_async
    def save_message_in_db(self, message):
        chat = PrivateChat.objects.get(id=self.private_chat[2])
        target_user = User.objects.get(username=self.target_username)
        PrivateMessage.objects.create(sender=self.scope['user'], receiver=target_user, chat=chat, text=message)
    
    
    # async def sendMessageChat(self, event):