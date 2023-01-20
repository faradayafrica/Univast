# Stdlib Imports
from random import randint

# Django Imports
from django.urls import reverse

# Rest Framework Imports
from rest_framework.test import APIClient, APITestCase

# Own Imports
from academia.models import Country, School, Faculty, Department


class BaseTestCase(APITestCase):
    """Base test case to setup fixtures."""

    def create_countries(self):
        """This method is responsible for creating countries fixtures."""

        return Country.objects.bulk_create(
            [
                Country(
                    id=randint(0, 999),
                    name="Argentina",
                    continent="South America",
                    country_code="ARG",
                ),
                Country(
                    id=randint(0, 999),
                    name="London",
                    continent="Europe",
                    country_code="UK",
                ),
                Country(
                    id=randint(0, 999),
                    name="Nigeria",
                    continent="Africa",
                    country_code="NG",
                ),
            ]
        )

    def create_schools(self):
        """This method is responsible for creating schools fixtures."""

        return School.objects.bulk_create(
            [
                School(
                    id=randint(0, 999),
                    listed=False,
                    type="Public",
                    name="Lagos Statue University",
                    code="LASU",
                    founded=1832,
                    ownership="Public",
                ),
                School(
                    id=randint(0, 999),
                    listed=False,
                    type="Private",
                    name="ALX Africa",
                    code="ALX",
                    founded=2020,
                    ownership="Private",
                ),
            ]
        )

    