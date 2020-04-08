from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Address
from django.urls import reverse

User = get_user_model()

class TestUsers(TestCase):

    def test_address_list_page_returns_only_owned(self):
        user1 = User.objects.create_user("user1", "testpass1")
        user2 = User.objects.create_user("user2", "testpass1")
        Address.objects.create(
            user = user1,
            name = "John Doe",
            address1 = "flat 1",
            address2 = "starlz avenue",
            city = "London",
            country = "uk"
        )

        Address.objects.create(
            user = user2,
            name = "Sam Foo",
            address1 = "flat 2",
            address2 = "queens avenue",
            city = "Brooklyn",
            country = "us"
        )

        self.client.force_login(user2)
        res = self.client.get(reverse("address_list"))
        self.assertEqual(res.status_code, 200)
        address_list = Address.objects.filter(user = user2)
        self.assertEqual(list(res.context["object_list"]), list(address_list))

    def test_address_create_stores_user(self):
        user1 = User.objects.create_user("user1", "testpass123")
        post_data = {
            "name" : "john kercher",
            "address1" : "1st asv st",
            "address2" : "",
            "zip_code" : "Blabla",
            "city" : "Manchester",
            "country" : "uk"
        }
        self.client.force_login(user1)
        self.client.post(reverse("address_create"), post_data)
        self.assertTrue(Address.objects.filter(user = user1).exists())
