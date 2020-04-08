from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from django.contrib import auth

from main import forms
from main.models import Product, ProductTag, ProductImage, Basket, BasketLine


from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.signals import setting_changed
from django.dispatch import receiver

User = get_user_model()

class TestPage(TestCase):

    def test_home_page(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'main/home.html')
        self.assertContains(res, 'hello')
        self.assertNotContains(res, 'I should not be here')

    def test_about_page(self):
        res = self.client.get(reverse('about_us'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'sells books')
        self.assertNotContains(res, 'I should not be here.')
        self.assertTemplateUsed(res, 'main/about_us.html')

    def test_contact_us_page_works(self):
        res = self.client.get(reverse('contact_us'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'main/contact.html')
        self.assertContains(res, 'Please fill')
        self.assertNotContains(res, 'I should not be here.')
        self.assertIsInstance(res.context['form'], forms.ContactForm)

    def test_products_page_returns_active(self):
        Product.objects.create(
            name = "The cathedral and the bazaar",
            slug = "the-cathedral-and-the-bazaar",
            price = Decimal(10.00)
            )

        Product.objects.create(
            name = "A tale of Two Cities",
            slug = "a-tale-of-two-cities",
            price = Decimal("2.00"),
            active = False
        )

        res = self.client.get(reverse('product_tags_list', kwargs = {"tag": "all"}))

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "BookTime")
        product_list = Product.objects.active().order_by("name")
        self.assertEqual(list(res.context["object_list"]), list(product_list))

    def test_products_page_filters_by_tags_and_active(self):
        cb = Product.objects.create(
            name = "The cathedral and the bazaar",
            slug = "the-cathedral-and-the-bazaar",
            price = Decimal("10.00"),
        )

        cb.tags.create(name = "Open source", slug = "open-source")
        Product.objects.create(
            name = "Microsoft Windows guide",
            slug = "microsoft-windows-guide",
            price = Decimal("12.00")
        )

        res = self.client.get(reverse("product_tags_list", kwargs = {"tag": "open-source"}))

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "BookTime")

        product_list = (Product.objects.active().filter(tags__slug="open-source").order_by("name"))
        self.assertEqual(list(res.context["object_list"]), list(product_list),)


    def test_add_to_basket_loggedin_works(self):
        user1 = User.objects.create_user("user1@a.com", "testpass123")
        cb = Product.objects.create(
            name = "The cathedral and the bazaar",
            slug = "the-cathedral-and-the-bazaar",
            price = Decimal("10.00"),
        )

        w = Product.objects.create(
            name = "Microsoft Windows guide",
            slug = "microsoft-windows-guide",
            price = Decimal("12.00"),
        )

        self.client.force_login(user1)
        res = self.client.get(reverse("add_to_basket"), {"product_id" : cb.id})
        self.assertTrue(Basket.objects.filter(user = user1).exists())
        self.assertEquals(BasketLine.objects.filter(basket__user = user1).count(), 1, )
        res = self.client.get(reverse("add_to_basket"), {"product_id" : w.id})
        self.assertEquals(BasketLine.objects.filter(basket__user = user1).count(), 2, )

    def test_add_to_basket_login_merge_works(self):
        user1 = User.objects.create_user(
            "user1@a.com", "pw432joij"
        )
        cb = Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        w = Product.objects.create(
            name="Microsoft Windows guide",
            slug="microsoft-windows-guide",
            price=Decimal("12.00"),
        )
        basket = Basket.objects.create(user=user1)
        BasketLine.objects.create(
            basket=basket, product=cb, quantity=2
        )
        BasketLine.objects.create(
            basket=basket, product=w, quantity=1
        )

        # response = self.client.post(
        #     reverse("account_login"),
        #     {"email": "user1@a.com", "password": "pw432joij"},
        # )

        self.client.force_login(user1)

        self.assertTrue(
            auth.get_user(self.client).is_authenticated
        )
        self.assertTrue(
            Basket.objects.filter(user=user1).exists()
        )
        basket = Basket.objects.get(user=user1)
        self.assertEquals(basket.count(),3)
