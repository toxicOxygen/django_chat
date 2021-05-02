from django.urls import re_path
from .consumer import ChatConsumer, GroupChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/user/(?P<user_id>\d+)/$', ChatConsumer),
    re_path(r'ws/chat/room/(?P<room_name>\w+)/$', GroupChatConsumer)
]

