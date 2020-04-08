from django.urls import path
from . import consumers
from channels.auth import AuthMiddlewareStack
from booktime.auth import TokenGetAuthMiddlewareStack

websocket_urlpatterns = [
    path(
        "ws/customer-service/<int:order_id>/",
        consumers.ChatConsumer
    )
]

http_urlpatterns = [
    path(
        "customer-service/notify/",
        AuthMiddlewareStack(
        consumers.ChatNotifyConsumer
        )
    ),
    path(
        "api/mobile-api/my-orders/<int:order_id>/tracker/",
        TokenGetAuthMiddlewareStack(
        consumers.OrderTrackerConsumer
        ),
    )
]
