from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Count, Sum

from django.contrib.auth import get_user_model

import logging
logger = logging.getLogger(__name__)

class ProductTagManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug = slug)

class ProductTag(models.Model):
    name = models.CharField(max_length = 32)
    slug = models.SlugField(max_length = 48)
    description = models.TextField(blank = True)
    active = models.BooleanField(default = True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug, )


class ActiveManager(models.Manager):

    def active(self):
        return self.filter(active = True)

class Product(models.Model):
    name = models.CharField(max_length = 32)
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    slug = models.SlugField(max_length = 48)
    tags = models.ManyToManyField(ProductTag, blank = True)
    active = models.BooleanField(default = True)
    in_stock = models.BooleanField(default = True)
    date_updated = models.DateTimeField(auto_now = True)

    objects = ActiveManager()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = "product-images")
    thumbnail = models.ImageField(upload_to = "product-thumbnails", null = True)


class Basket(models.Model):
    OPEN = 10
    SUBMITTED = 20
    STATUSES = ((OPEN, "Open"), (SUBMITTED, "Submitted"))
    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE, blank = True, null = True)
    status = models.IntegerField(choices = STATUSES, default = OPEN)

    def is_empty(self):
        return self.basketline_set.all().count() == 0

    def count(self):
        return sum(i.quantity for i in self.basketline_set.all())

    def create_order(self, billing_address, shipping_address):
        if not self.user:
            raise exceptions.BasketException("Cannot create order without user.")
        logger.info("Creating order for basket_id=%d"", shipping_address_id = %d, billing_address_id = %d", self.id, shipping_address.id, billing_address.id)
        order_data = {
            "user": self.user,
            "billing_name": billing_address.name,
            "billing_address1": billing_address.address1,
            "billing_address2": billing_address.address2,
            "billing_zip_code": billing_address.zip_code,
            "billing_city": billing_address.city,
            "billing_country": billing_address.country,
            "shipping_name": shipping_address.name,
            "shipping_address1": shipping_address.address1,
            "shipping_address2": shipping_address.address2,
            "shipping_zip_code": shipping_address.zip_code,
            "shipping_city": shipping_address.city,
            "shipping_country": shipping_address.country,
        }
        order = Order.objects.create(**order_data)
        c = 0
        for line in self.basketline_set.all():
            for item in range(line.quantity):
                order_line_data = {
                    "order": order,
                    "product": line.product,
                }
                order_line = OrderLine.objects.create(**order_line_data)
                c += 1
        logger.info("Created order with id=%d and line_count =%d", order.id, c)
        self.status = Basket.SUBMITTED
        self.save()
        return order

class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1, validators = [MinValueValidator(1)])

class Order(models.Model):
    NEW = 10
    PAID = 20
    DONE = 30
    STATUSES = ((NEW, "New"), (PAID, "Paid"), (DONE, "Done"))

    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    status = models.IntegerField(choices = STATUSES, default = NEW)

    billing_name = models.CharField(max_length = 60)
    billing_address1 = models.CharField(max_length = 60)
    billing_address2 = models.CharField(max_length = 60, blank = True)
    billing_zip_code = models.CharField(max_length = 12)
    billing_city = models.CharField(max_length = 60)
    billing_country = models.CharField(max_length = 3)

    shipping_name = models.CharField(max_length = 60)
    shipping_address1 = models.CharField(max_length = 60)
    shipping_address2 = models.CharField(max_length = 60, blank = True)
    shipping_zip_code = models.CharField(max_length = 60)
    shipping_city = models.CharField(max_length = 60)
    shipping_country = models.CharField(max_length = 3)

    date_updated = models.DateTimeField(auto_now = True)
    date_added = models.DateTimeField(auto_now_add = True)

    last_spoken_to = models.ForeignKey(get_user_model(), null = True, related_name = "cs_chats", on_delete = models.SET_NULL)

    def __str__(self):
        return f'Order: {self.id} - {self.user}'

    @property
    def mobile_thumb_url(self):
        products = [i.product for i in self.lines.all()]
        if products:
            img = products[0].productimage_set.first()
            if img:
                return img.thumbnail.url

    @property
    def summary(self):
        product_counts = self.lines.values("product__name").annotate(c=Count("product__name"))
        pieces = []
        for pc in product_counts:
            pieces.append("%s x %s" % (pc["c"], pc["product__name"]))
        return ", ".join(pieces)

    @property
    def total_price(self):
        res = self.lines.aggregate(total_price = Sum("product__price"))
        return res["total_price"]

class OrderLine(models.Model):
    NEW = 10
    PROCESSING = 20
    SENT = 30
    CANCELLED = 40
    STATUSES = ((NEW, "New"), (PROCESSING, "Processing"), (SENT, "Sent"), (CANCELLED, "Cancelled"))

    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = "lines")
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    status = models.IntegerField(choices = STATUSES, default = NEW)
