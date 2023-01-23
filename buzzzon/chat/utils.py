from channels.db import database_sync_to_async

from . import models


@database_sync_to_async
def create_chat_message(sender, receiver_id, message):
    content = message['content']
    return models.Message.objects.create(sender=sender, receiver_id=receiver_id, content=content)
