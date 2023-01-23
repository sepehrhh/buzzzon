from channels.db import database_sync_to_async
from django.db.models import Q

from . import models


@database_sync_to_async
def create_chat_message(sender, receiver_id, message):
    content = message['content']
    message_type = message['type']
    return models.Message.objects.create(sender=sender, receiver_id=receiver_id,
                                         content=content, type=message_type)


@database_sync_to_async
def create_group_chat_message(sender, group, message):
    content = message['content']
    message_type = message['type']
    return models.Message.objects.create(sender=sender, group=group,
                                         content=content, type=message_type)


@database_sync_to_async
def get_group(share_code, user):
    return models.Group.objects.filter(Q(share_code=share_code) &
                                       (Q(participants__id=user.id) | Q(owner_id=user.id))).distinct().first()
