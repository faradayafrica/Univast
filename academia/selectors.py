# Rest Framework Imports
from rest_framework import exceptions

# Own Imports
from academia.models import School, Country, Faculty


def get_school(code: str) -> str:
    """
    This function checks if a school exist with the provided code,
    raises an NotFound except if it does not.

    :param code: This is the school code that we want
        to get the school for
    :type code: str

    :return: The school code.
    """

    if not School.objects.filter(code=code).exists():
        raise exceptions.NotFound({"message": "School not found!"})
    return code


def get_country(code: str) -> str:
    """
    This function returns the country code if it exists,
    otherwise it raises a NotFound exception.

    :param code: This is the code associated with the name of the country we want
    :type code: str

    :return: The country code.
    """

    if code.lower():
        code = code.upper()
    if not Country.objects.filter(country_code=code).exists():
        print(code.lower())
        raise exceptions.NotFound({"message": "Country not found!"})
    return code


def get_faculty(name: str) -> str:
    """
    This function returns the faculty name if it exists,
    otherwise it raises a NotFound exception.

    :param name: The name of the faculty we want
    :type name: str
    """

    if not Faculty.objects.filter(name__lower=name).exists():
        raise exceptions.NotFound({"message": "Faculty not found!"})
    return name
