import factory
import factory.fuzzy
from . import models

from users.models import Address, User
from django.contrib.auth import get_user_model

class UserFactory(factory.django.DjangoModelFactory):
    email = "user@site.com"
    password ="testoass123",

    class Meta:
        model = get_user_model()
        django_get_or_create = ("email", "password")


class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.fuzzy.FuzzyDecimal(1.0, 1000.0, 2)

    class Meta:
        model = models.Product


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address


class OrderLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OrderLine


class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Order
