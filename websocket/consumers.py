from channels.generic.websocket import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from user.models import User
from chatapp.models import PrivateChat, PrivateMessage, GroupChat, GroupMessage
from urllib.parse import parse_qs
import json
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
            
            # send message to group(user1 and user2)
            await self.channel_layer.group_send(
                f'private_chat_{self.private_chat[0]}_{self.private_chat[1]}',
                {
                    'type': 'sendMessageGroup',
                    'message': json.dumps({'sender': self.scope['user'].username, 'receiver': self.target_username, 'text': message, 'date_time': datetime.now()}, cls=DateTimeJsonEncoder)
                }
            )
            await self.save_message_in_db(message)
            
            # send a notification for user1 and user2
            users_list = [self.private_chat[3], self.private_chat[4]]
            for pk in users_list:
                await self.channel_layer.group_send(
                    f'user_notification_{pk}',
                    {
                        'type': 'sendNotification',
                        'message': json.dumps({
                            'type': 'private_chat',
                            'text': message,
                            'sender': self.scope['user'].username,
                            'send_time': datetime.now(),
                            'id': self.private_chat[2],
                        }, cls=DateTimeJsonEncoder)
                    }
                )
    
    
    async def sendMessageGroup(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

            

    @database_sync_to_async
    def user_private_chat(self, target_username, requested_user):
        try:
            p = PrivateChat.objects.get(Q(user1__username=requested_user, user2__username=target_username) | Q(user1__username=target_username, user2__username=requested_user))
            return [p.user1.username, p.user2.username, p.pk, p.user1.pk, p.user2.pk]
        except PrivateChat.DoesNotExist:
            return None
    
    @database_sync_to_async
    def save_message_in_db(self, message):
        chat = PrivateChat.objects.get(id=self.private_chat[2])
        target_user = User.objects.get(username=self.target_username)
        PrivateMessage.objects.create(sender=self.scope['user'], receiver=target_user, chat=chat, text=message)


async def send_message_group(chat, channel_layer, message_type, message=None, sender=None, receiver=None, sender_name=None):
    if message_type == 'update' or chat['can_send_message'] == True or sender == chat['manager']:
        await channel_layer.group_send(
            f"group_chat_{chat['address']}",
            {
                'type': 'sendMessageGroup',
                'message': json.dumps({'type': message_type, 'text': message, 'sender': sender, 'sender_name': sender_name, 'receiver': receiver, 'chat': chat, 'send_time': datetime.now()}, cls=DateTimeJsonEncoder)
            }
        )


class GroupChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        group_address = parse_qs(self.scope['query_string'].decode('utf8'))['address'][0]
        self.chat = await self.get_group_chat(group_address)
        self.user = self.scope['user']
        self.group_address = f"group_chat_{self.chat['address']}"

        if self.user.is_authenticated:
            if self.user.username in self.chat['members'].keys():
                await self.send({
                    'type': 'websocket.accept'
                })
                await self.channel_layer.group_add(
                    self.group_address,
                    self.channel_name
                )
            else:
                await self.send({
                    'type': 'websocket.close'
                })
        else:
            await self.send({
                'type': 'websocket.close'
            })

    async def websocket_disconnect(self, message):
        await self.send({
            'type': 'websocket.close'
        })
        raise StopConsumer()

    async def websocket_receive(self, text_data = None, bytes_data=None):
        if text_data:
            text_data_loaded = json.loads(text_data['text'])
            if text_data_loaded['type'] == 'msg':
                await self.save_message_in_db(text_data_loaded['type'], self.chat['id'], text_data_loaded['message'], self.user.username)
                await send_message_group(self.chat, self.channel_layer, text_data_loaded['type'], text_data_loaded['message'], self.user.username)

                # send notification for all members
                members = self.chat['members']
                for user in members.keys():
                    await self.channel_layer.group_send(
                        f"user_notification_{members[user]['id']}",
                        {
                            'type': 'sendNotification',
                            'message': json.dumps({
                                'type': 'group_chat',
                                'text': text_data_loaded['message'],
                                'group': {
                                    'id': self.chat['id'],
                                    'address': self.chat['address'],
                                    'name': self.chat['name'],
                                    'sender': self.user.username
                                    }
                                })
                        }
                    )
    
    @database_sync_to_async
    def save_message_in_db(self, message_type, group_id, message=None, sender=None, receiver=None):
        GroupMessage.objects.create(message_type=message_type, text=message, sender=self.user, chat_id=group_id)
    
    @database_sync_to_async    
    def get_group_chat(self, group_address):
        try:
            g = GroupChat.objects.get(address=group_address)
            chat = {
                'members': g.get_all_members(),
                'address': g.address,
                'manager': g.manager.username,
                'id': g.id,
                'name': g.name,
                'can_send_message': g.can_send_message,
            }
            return chat
        except GroupChat.DoesNotExist:
            return None
    
    async def sendMessageGroup(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })


class NotificationConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.send({
                'type': 'websocket.accept'
            })
            await self.channel_layer.group_add(
                f'user_notification_{self.user.id}',
                self.channel_name
            )
        else:
            self.send({
                'type': 'websocket.close'
            })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            f"user_notification_{self.user.id}",
            self.channel_name
        )
        raise StopConsumer()
    
    async def sendNotification(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })