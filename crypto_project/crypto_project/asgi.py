import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crypto_project.settings")
django_asgi_app = get_asgi_application()

from crypto.routing import websocket_urlpatterns  # noqa E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)


def get_application():
    """
    Returns the ASGI application callable.
    """
    return application
