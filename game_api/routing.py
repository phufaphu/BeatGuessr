from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/import-logs/(?P<playlist_id>\w+)/$', consumers.ImportLogConsumer.as_asgi()),
]