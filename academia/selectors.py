# Rest Framework Imports
from rest_framework import exceptions

# Own Imports
from academia.models import School


def get_school(country: str) -> School:
    """
    This function checks if a school exist for the provided country,
    raises an NotFound except if it does not.

    :param country: str - This is the country name that we want
        to get the school for
    :type country: str

    :return: A school object
    """

    school = School.objects.filter(country__name=country).first()

    if school is None:
        raise exceptions.NotFound({"message": "School does not exist!"})
    return school
