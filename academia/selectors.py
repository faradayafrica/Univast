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
        raise exceptions.NotFound({"message": "School does not exist!"})
    return code


def get_country(name: str) -> str:
    """
    This function returns the country name if it exists,
    otherwise it raises a NotFound exception.

    :param name: This is the name of the country we want
    :type name: str

    :return: The country name.
    """

    if not Country.objects.filter(name=name).exists():
        raise exceptions.NotFound({"message": "Country not found!"})
    return name


def get_faculty(name: str) -> str:
    """
    This function returns the faculty name if it exists,
    otherwise it raises a NotFound exception.
    
    :param name: The name of the faculty we want
    :type name: str
    """
    
    if not Faculty.objects.filter(name=name).exists():
        raise exceptions.NotFound({"message": "Faculty not found!"})
    return name