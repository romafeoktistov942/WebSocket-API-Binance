from django.urls import path
from .consumers import CryptoConsumer

websocket_urlpatterns = [
    path("ws/prices/", CryptoConsumer.as_asgi()),
]
