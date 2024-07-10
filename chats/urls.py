from django.utils.timezone import now
from core.wsgi import sio
from chats.models import Chat, ChatMessage
from django.urls import path

from chats.views.chats import ChatsView, ChatView
from chats.views.messages import ChatMessagesView, ChatMessageView

urlpatterns = [
    path('', ChatsView.as_view()),
    path('<int:chat_id>', ChatView.as_view()),
    path('<int:chat_id>/messages', ChatMessagesView.as_view()),
    path('<int:chat_id>/messages/<int:message_id>', ChatMessageView.as_view()),
]

# Sockets events handlers
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
