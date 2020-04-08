from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views
from channels.auth import AuthMiddlewareStack
from . import endpoints
from main import consumers

router = routers.DefaultRouter()
router.register(r'orderlines', endpoints.PaidOrderLineViewSet)
router.register(r'order', endpoints.PaidOrderViewSet)
router.register(r'products', endpoints.ProductsViewSet)
router.register(r'tags', endpoints.TagsViewSet)
router.register(r'product-images', endpoints.ImageProductViewset)

urlpatterns = [
    path('employees-api/', include(router.urls)),

    path('api-auth/', include('rest_framework.urls')),

    path('mobile-api/', authtoken_views.obtain_auth_token, name="mobile_token"),
    path('mobile-api/my-orders/', endpoints.my_orders, name="mobile_my_orders"),
    path("mobile-api/my-orders/<int:order_id>/tracker/", AuthMiddlewareStack(consumers.OrderTrackerConsumer),)
]
