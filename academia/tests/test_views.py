# Stdlib Imports
from random import randint

# Django Imports
from django.urls import reverse
from django.db.models import QuerySet

# Rest Framework Imports
from rest_framework.test import APIClient, APITestCase

# Third Party Imports
from rest_framework_api_key.models import APIKey

# Own Imports
from academia.models import Country, School, Faculty, Department, Degree


class BaseTestCase(object):
    """Base test case to setup fixtures."""

    @classmethod
    def create_countries(cls) -> QuerySet[Country]:
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
    def create_schools(cls) -> QuerySet[School]:
        """This method is responsible for creating schools fixtures."""

        country = cls.create_countries()[2]
        return School.objects.bulk_create(
            [
                School(
                    unlisted=False,
                    type="Public",
                    name="Lagos Statue University",
                    code="LASU",
                    founded=1832,
                    country=country,
                    ownership="Public",
                ),
                School(
                    unlisted=False,
                    type="Private",
                    name="ALX Africa",
                    code="ALX",
                    founded=2020,
                    country=country,
                    ownership="Private",
                ),
            ]
        )

    @classmethod
    def create_faculties(cls) -> QuerySet[Faculty]:
        """This method is responsible for creating school faculties fixtures."""

        alx_africa = cls.create_schools()[1]
        return Faculty.objects.bulk_create(
            [
                Faculty(school=alx_africa, name="Frontend Engineering"),
                Faculty(school=alx_africa, name="Backend Engineering"),
                Faculty(school=alx_africa, name="Product Management"),
            ]
        )
        
    @classmethod
    def create_degrees(cls) -> QuerySet[Degree]:
        """This method is responsible for creating degrees fixtures."""
        
        return Degree.objects.bulk_create(
            [
                Degree(name="Bachelor of Science", code="B.Sc"),
                Degree(name="Bachelor of Technology", code="B.Tech")
            ]
        )

    @classmethod
    def create_departments(cls) -> QuerySet[Department]:
        """This method is responsible for creating departments in a school faculty."""

        alx_africa = cls.create_schools()[1]
        bck_eng = cls.create_faculties()[1]
        degrees = cls.create_degrees()

        return Department.objects.bulk_create(
            [
                Department(
                    school=alx_africa,
                    faculty=bck_eng,
                    degree=degrees[0],
                    name="JavaScript/TypeScript + NodeJS + MongoDB",
                ),
                Department(
                    school=alx_africa,
                    faculty=bck_eng,
                    degree=degrees[1],
                    name="Python + Django + PostgreSQL",
                ),
            ]
        )
        
    @classmethod
    def get_user_apikey(cls) -> dict:
        """
        This method is responsible for creating an API key.

        :param cls: The class of the test case
        :return: The headers are being returned.
        """

        _, api_key = APIKey.objects.create_key(
            name="Test", expiry_date="2029-01-30 2:00:00"
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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], True)
        self.assertEqual(len(response.data["data"]), 3)


class SchoolListAPITestCase(APITestCase):
    def setUp(self) -> None:
        """Setup fixtures for school list api test case."""

        self.country = BaseTestCase.create_countries()[2]
        self.country.save()

        self.schools = BaseTestCase.create_schools()
        self.client = APIClient()

    def test_get_list_of_schools(self):
        """Ensure we get a list of schools."""

        url = reverse("academia:get_schools", args=[self.country.country_code])
        response = self.client.get(
            url, format="json", **BaseTestCase.get_user_apikey()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], True)
        self.assertEqual(len(response.data["data"]), 2)


class SchoolFacultyAPITestCase(APITestCase):
    def setUp(self) -> None:
        """Setup fixtures for school faculties api test case."""

        self.school = BaseTestCase.create_schools()[1]
        self.school.save()

        self.faculties = BaseTestCase.create_faculties()
        self.client = APIClient()

    def test_get_list_of_school_faculties(self):
        """Ensure we get a list of school faculties."""

        url = reverse("academia:get_faculties", args=[self.school.code])
        response = self.client.get(
            url, format="json", **BaseTestCase.get_user_apikey()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], True)
        self.assertEqual(len(response.data["data"]), 3)


class DepartmentListAPITestCase(APITestCase):
    def setUp(self) -> None:
        """Setup fixtures for department lst api test case."""

        self.nd = Degree.objects.create(name="National Diploma", code="ND")

        self.school = BaseTestCase.create_schools()[1]
        self.school.save()

        self.bck_eng = BaseTestCase.create_faculties()[1]
        self.bck_eng.save()

        self.departments = BaseTestCase.create_departments()

        self.client = APIClient()

    def test_get_list_of_departments(self):
        """Ensure we get a list of departments."""

        url = reverse(
            "academia:get_departments",
            args=[self.school.code, self.bck_eng.name],
        )
        response = self.client.get(
            url, format="json", **BaseTestCase.get_user_apikey()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], True)
        self.assertEqual(len(response.data["data"]), 2)
