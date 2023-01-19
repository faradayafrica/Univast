# Rest Framework Imports
from rest_framework import exceptions

# Own Imports
from academia.models import School, Country


def get_school(code: str) -> str:
    """
    This function checks if a school exist with the provided code,
    raises an NotFound except if it does not.

    :param code: str - This is the school code that we want
        to get the school for
    :type code: str

    :return: The school code.
    """

    if not School.objects.filter(code=code).exists():
        raise exceptions.NotFound({"message": "School does not exist!"})
    return code


def get_country(country: str) -> str:
    """
    This function returns the country name if it exists,
    otherwise it raises a NotFound exception.

    :param country: str - This is the parameter that will be passed in the URL
    :type country: str

    :return: The country name.
    """

    if not Country.objects.filter(name=country).exists():
        raise exceptions.NotFound({"message": "Country not found!"})
    return country
