from rest_framework import serializers, viewsets
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from main import models
from .serializers import OrderSerializer, OrderLineSerializer, ProductsSerializer, TagsSerializer, ImageProductSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = models.Product.objects.filter().order_by("-id")
    serializer_class = ProductsSerializer

class TagsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = models.ProductTag.objects.filter().order_by("-id")
    serializer_class = TagsSerializer

class ImageProductViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = models.ProductImage.objects.filter().order_by("-product")
    serializer_class = ImageProductSerializer

class PaidOrderLineViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = models.OrderLine.objects.filter(
        order__status=models.Order.PAID
    ).order_by("-order__date_added")

    serializer_class = OrderLineSerializer
    filter_fields = ("order", "status")
    http_method_names = ['get']

class PaidOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = models.Order.objects.filter(
        status=models.Order.PAID
    ).order_by("-date_added")
    serializer_class = OrderSerializer
    http_method_names = ['get']

@api_view()
@permission_classes((IsAuthenticated,))
def my_orders(request):
    user = request.user
    orders = models.Order.objects.filter(user = user).order_by("-date_added")
    data = []
    for order in orders:
        data.append(
            {
                "id": order.id,
                "image": order.mobile_thumb_url,
                "summary": order.summary,
                "price": order.total_price,
            }
        )
    return Response(data)
