# Stdlib Imports
from random import randint

# Django Imports
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Rest Framework Imports
from rest_framework.test import APIClient, APITestCase

# Third Party Imports
from rest_framework_api_key.models import APIKey

# Own Imports
from academia.models import Country, School, Faculty, Department


class BaseTestCase(object):
    """Base test case to setup fixtures."""

    @classmethod
    def create_countries(cls):
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

    @classmethod
    def create_schools(cls):
        """This method is responsible for creating schools fixtures."""

        return School.objects.bulk_create(
            [
                School(
                    listed=False,
                    type="Public",
                    name="Lagos Statue University",
                    code="LASU",
                    founded=1832,
                    ownership="Public",
                ),
                School(
                    listed=False,
                    type="Private",
                    name="ALX Africa",
                    code="ALX",
                    founded=2020,
                    ownership="Private",
                ),
            ]
        )

    @classmethod
    def create_user(cls) -> User:
        """
        This method is responsible for creating a test user.

        :param cls: The class of the test case
        :return: The user that was created.
        """

        return User.objects.get_or_create(
            first_name="Test",
            last_name="User",
            email="testuser@email.com",
            username="testuser",
            password=make_password("testuser__#%D^#GVD^@#G"),
        )[0]

    @classmethod
    def get_user_apikey(cls) -> str:
        """
        This method is responsible for creating an API key.

        :param cls: The class of the test case
        :return: The headers are being returned.
        """

        _, api_key = APIKey.objects.create_key(
            name="Test", expiry_date="2023-01-30 2:00:00"
        )
        headers = {"HTTP_AUTHORIZATION": f"Api-Key {api_key}"}
        return headers


class CountryListAPITestCase(APITestCase):
    def setUp(self) -> None:
        """Setup fixtures for country list api test case."""

        self.countries = BaseTestCase.create_countries()
        self.client = APIClient()

    def test_get_list_of_countries(self):
        """Ensure we get a list of countries."""

        url = reverse("academia:get_countries")
        response = self.client.get(
            url, format="json", **BaseTestCase.get_user_apikey()
        )

        print("Content: ", response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], True)
        self.assertEqual(len(response.data["data"]), 3)
