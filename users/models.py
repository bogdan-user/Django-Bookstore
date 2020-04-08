from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):

    @property
    def is_employee(self):
        return self.is_active and (self.is_superuser or self.is_staff and self.groups.filter(name="Employees").exists())

    @property
    def is_dispatcher(self):
        return self.is_active and (self.is_superuser or self.is_staff and self.groups.filter(name="Dispatchers").exists())

    def __str__(self):
        return self.username

class Address(models.Model):
    SUPPORTED_COUTNRIES = (
        ("uk", "United Kingdom"),
        ("us", "United States of America"),
    )

    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    name = models.CharField(max_length = 60)
    address1 = models.CharField("Address line 1", max_length = 60)
    address2 = models.CharField("Address line 2", max_length = 60, blank = True)
    zip_code = models.CharField("ZIP / Postal code", max_length = 12)
    city = models.CharField(max_length = 60)
    country = models.CharField(max_length = 3, choices = SUPPORTED_COUTNRIES)

    def __str__(self):
        return ", ".join(
                [
                    self.name,
                    self.address1,
                    self.address2,
                    self.zip_code,
                    self.city,
                    self.country,
                ]
        )
