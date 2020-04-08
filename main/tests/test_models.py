from decimal import Decimal
from django.test import TestCase
from main import models
from main.models import Product, Basket, BasketLine
from users.models import Address
from main import factories
from django.contrib.auth import get_user_model

User = get_user_model()

#
# class TestModel(TestCase):
#     def test_active_manager_works(self):
#         models.Product.objects.create(
#             name = "The cathedral and the bazaar",
#             price = Decimal("10.00")
#         )
#         models.Product.objects.create(
#             name = "Pride and Prejudice",
#             price = Decimal("2.00")
#         )
#         models.Product.objects.create(
#             name = "A tale of Two Cities",
#             price = Decimal("2.00"),
#             active = False
#         )
#
#         self.assertEqual(len(models.Product.objects.active()), 2)
#
#     def test_create_order_works(self):
#         p1 = Product.objects.create(
#             name = "The cathedral and the bazaar",
#             price = Decimal("10.00")
#         )
#         p2 = Product.objects.create(
#             name = "Pride and prejudice",
#             price = Decimal("2.00")
#         )
#         user1 = User.objects.create_user(
#             "user1", "testpass123"
#         )
#         billing = Address.objects.create(
#             user = user1,
#             name = "Sam Doe",
#             address1 = "An address is here",
#             city = "London",
#             country = "uk",
#         )
#         shipping = Address.objects.create(
#             user = user1,
#             name = "Sam Doe",
#             address1 = "Shipping address here",
#             city = "London",
#             country = "uk",
#         )
#         basket = Basket.objects.create(user = user1)
#         BasketLine.objects.create(
#             basket = basket, product = p1
#         )
#         BasketLine.objects.create(
#             basket = basket, product = p2
#         )
#
#         with self.assertLogs("main.models", level ="INFO") as cm:
#             order = basket.create_order(billing, shipping)
#         self.assertGreaterEqual(len(cm.output), 1)
#
#         order.refresh_from_db()
#
#         self.assertEquals(order.user, user1)
#         self.assertEquals(
#             order.billing_address1, "An address is here"
#         )
#         self.assertEquals(
#             order.shipping_address1, "Shipping address here"
#         )
#         self.assertEquals(order.lines.all().count(), 2)
#         lines = order.lines.all()
#         self.assertEquals(lines[0].product, p1)
#         self.assertEquals(lines[1].product, p2)

class TestModel(TestCase):

    def test_active_manager_works(self):
        factories.ProductFactory.create_batch(2, active = True)
        factories.ProductFactory(active = False)
        self.assertEqual(len(models.Product.objects.active()), 2)

    def test_create_order_works(self):
        p1 = factories.ProductFactory()
        p2 = factories.ProductFactory()
        user1 = factories.UserFactory()
        billing = factories.AddressFactory(user = user1)
        shipping = factories.AddressFactory(user = user1)

        basket = models.Basket.objects.create(user=user1)
        models.BasketLine.objects.create(
            basket = basket, product = p1
        )
        models.BasketLine.objects.create(
            basket = basket, product = p2
        )

        with self.assertLogs("main.models", level = "INFO") as cm:
            order = basket.create_order(billing, shipping)

        self.assertGreaterEqual(len(cm.output), 1)

        order.refresh_from_db()

        self.assertEquals(order.user, user1)
        self.assertEquals(order.billing_address1, billing.address1)
        self.assertEquals(order.shipping_address1, shipping.address1)

        self.assertEquals(order.lines.all().count(), 2)
        lines = order.lines.all()
        self.assertEquals(lines[0].product, p1)
        self.assertEquals(lines[1].product, p2)
