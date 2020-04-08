from django.urls import reverse
from rest_framework.test import APITestCase
from main import models, factories
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

class TestEndpoints(APITestCase):
    def test_mobile_login_works(self):
        user = User.objects.create_user(
            username="user1", email="user1@email.com", password="abcabcabc"
        )
        response = self.client.post(
            reverse("mobile_token"),
            {"username": "user1", "email":"user1@email.com", "password": "abcabcabc"},
        )
        jsonresp = response.json()
        self.assertIn("token", jsonresp)

    def test_mobile_flow(self):
        user = User.objects.create_user(username="mobileuser", email="mobileuser@email.com", password="testpass123")

        token = Token.objects.get(user=user)

        self.client.credentials (HTTP_AUTHORIZATION = "Token " + token.key)
        orders = factories.OrderFactory.create_batch(2, user=user)
        a = factories.ProductFactory(name = "The book of A", active = True, price = 12.00)
        b = factories.ProductFactory(name = "The book of B", active = True, price = 14.00)
        factories.OrderLineFactory.create_batch(2, order = orders[0], product = a)
        factories.OrderLineFactory.create_batch(2, order = orders[1], product = b)
        response = self.client.get(reverse("mobile_my_orders"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [
            {
                "id": orders[1].id,
                "image": None,
                "price": 28.0,
                "summary": "2 x The book of B",
            },
            {
                "id": orders[0].id,
                "image": None,
                "price": 24.0,
                "summary": "2 x The book of A",
            },
        ]
        self.assertEqual(response.json(), expected)
