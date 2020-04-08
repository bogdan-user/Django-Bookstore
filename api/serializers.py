from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from main import models

class TagsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = [IsAdminUser]
    fields = "__all__"

    class Meta:
        model = models.ProductTag
        fields = "__all__"

class ImageProductSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = [IsAdminUser]

    class Meta:
        model = models.ProductImage
        fields = "__all__"

class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = [IsAdminUser]
    class Meta:
        model = models.Product
        fields = "__all__"
        depth = 2

class OrderSerializer(serializers.ModelSerializer):
    permission_classes = [IsAdminUser]
    class Meta:
        model = models.Order
        fields = (
            "status",
            "shipping_name",
            "shipping_address1",
            "shipping_address2",
            "shipping_zip_code",
            "shipping_city",
            "shipping_country",
            "date_updated",
            "date_added",
        )
        # fields = "__all__"

class OrderLineSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = [IsAdminUser]

    product = serializers.StringRelatedField()

    class Meta:
        model = models.OrderLine
        fields = ("id", "order", "product", "status")
