from channels.db import database_sync_to_async

from . import models


@database_sync_to_async
def create_chat_message(sender, receiver_id, message):
    content = message['content']
    message_type = message['type']
    return models.Message.objects.create(sender=sender, receiver_id=receiver_id,
                                         content=content, type=message_type)
