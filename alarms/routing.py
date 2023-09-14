from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/alarm/(?P<room_name>\w+)/$', consumers.AlarmConsumer.as_asgi()),
]