# Rest Framework Imports
from rest_framework import exceptions

# Own Imports
from academia.models import School, Country, Faculty


def get_school(school_id: str) -> str:
    """
    This function checks if a school exist with the provided id,
    raises an NotFound except if it does not.

    :param id: This is the school id that we want
        to get the school for
    :type id: str

    :return: The school id.
    """

    if not School.objects.filter(id=school_id).exists():
        raise exceptions.NotFound({"message": "School not found!"})
    return school_id


def get_country(country_id: str) -> str:
    """
    This function returns the country id if it exists,
    otherwise it raises a NotFound exception.

    :param id: This is the id associated with the name of the country we want
    :type id: str

    :return: The country id.
    """

    if not Country.objects.filter(id=country_id).exists():
        raise exceptions.NotFound({"message": f"Country not by id {country_id} not found!"})
    return country_id


def get_faculty(faculty_id: str) -> str:
    """
    This function returns the faculty id if it exists,
    otherwise it raises a NotFound exception.

    :param id: The id of the faculty we want
    :type id: str
    """

    if not Faculty.objects.filter(id=faculty_id).exists():
        raise exceptions.NotFound({"message": "Faculty not found!"})
    return faculty_id
