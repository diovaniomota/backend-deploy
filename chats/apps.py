from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chats'

    def ready(self) -> None: 
        from chats.models import Chat, ChatMessage
        from core.wsgi import sio
        from django.utils.timezone import now

        @sio.event
        def update_messages_as_seen(sid, data):
            chat_id = data.get('chat_id')

            # Getting chat
            chat = Chat.objects.values(
                'from_user_id',
                'to_user_id'
            ).filter(
                id=chat_id
            ).first()

            # Updating chat messages as viewed
            ChatMessage.objects.filter(
                chat_id=chat_id,
                viewed_at__isnull=True
            ).update(
                viewed_at=now()
            )

            # Sending update chat to users
            sio.emit('update_chat', {
                "query": {
                    "users": [chat['from_user_id'], chat['to_user_id']]
                }
            })

            # Update chat messages as seen
            sio.emit('mark_messages_as_seen', {
                "query": {
                    "chat_id": chat_id,
                    "exclude_user_id": data.get('exclude_user_id')
                }
            })

            return True
