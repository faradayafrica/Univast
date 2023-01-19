# Stdlib Imports
from typing import List

# Django imports
from django.shortcuts import render
from django.db.models import QuerySet

# Rest Framework Imports
from rest_framework.request import Request
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIKey

# Own imports
from academia.models import Country, School, Faculty, Department
from academia.serializers import (
    CountrySerializer,
    SchoolSerializer,
    FacultySerializer,
    DepartmentSerializer,
)
from academia.selectors import get_country, get_school

# Third Party Imports
from rest_api_payload import success_response, error_response


# Home page
def home(request):
    return render(request, "academia/index.html", {})


# Cutom 404 handler
def custom_page_not_found_view(request, exception):
    return render(request, "academia/404.html", {})


# Cutom 500 handler
def custom_error_view(request, exception=None):
    return render(request, "academia/500.html", {})


# Cutom 403 handler
def custom_permission_denied_view(request, exception=None):
    return render(request, "academia/403.html", {})


# Cutom 400 handler
def custom_bad_request_view(request, exception=None):
    return render(request, "academia/400.html", {})


class CountryListAPIView(generics.ListAPIView):
    serializer_class = CountrySerializer
    permission_classes = (HasAPIKey,)
    queryset = Country.objects.only("id", "name", "country_code")

    def get(self, request: Request) -> Response:
        """
        This API retrieves the list of countries (name and code).
        """

        countries = self.get_queryset()
        serializer = self.serializer_class(countries, many=True)

        payload = success_response(
            status=True,
            message="Retrieved all countries!",
            data=serializer.data,
        )
        return Response(payload, status=status.HTTP_200_OK)


class SchoolListAPIView(generics.ListAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (HasAPIKey,)
    queryset = School.objects.only(
        "id",
        "type",
        "name",
        "code",
        "website",
        "logo",
        "ownership",
        "owned_by",
        "founded",
        "address",
    )

    def get(self, request: Request) -> Response:
        """
        This API view retrieves the list of schools.

        :param country_name: the name of country you wish to get the list of available schools in.
        :type country_name: str
        """
        schools = self.get_queryset()
        serializer = self.serializer_class(
            schools, many=True, context={"request": request}
        )

        response = success_response(
            status=True,
            message=f"Retrieved all schools!",
            data=serializer.data,
        )
        return Response(data=response, status=status.HTTP_200_OK)

    def get_queryset(self) -> List[QuerySet]:
        # get query param from request
        qry_param = self.request.query_params

        # return queryset if query param is None
        # otherwise return queryset filtered by
        # the country name
        if not qry_param:
            return self.queryset.all()

        country = get_country(qry_param.get("country_name"))
        return self.queryset.filter(country__name=country)


class SchoolFacultyListAPIView(generics.ListAPIView):
    serializer_class = FacultySerializer
    permission_classes = (HasAPIKey,)
    queryset = Faculty.objects.only("id", "name")

    def get(self, request: Request, school_code: str) -> Response:
        """
        This API view retrieves the list of faculties in a school.

        :param school_code: the name of school you wish to get the list of available faculties in.
        :type school_code: str
        """
        schools = self.get_queryset(school_code)
        serializer = self.serializer_class(
            schools, many=True, context={"request": request}
        )

        response = success_response(
            status=True,
            message=f"Retrieved all faculties!",
            data=serializer.data,
        )
        return Response(data=response, status=status.HTTP_200_OK)

    def get_queryset(self, code: str) -> List[QuerySet]:
        school_code = get_school(code)
        return self.queryset.filter(school__code=school_code)


# Fetch all Departments in a Faculty.
@api_view(["GET"])
@permission_classes((HasAPIKey,))
def DepartmentList(request):
    # initialize empty array to hold error message(s)
    messages = {"errors": []}

    # get required parameters
    school_name = request.data.get("school")
    faculty_name = request.data.get("faculty")

    # perform validations for required parameters
    if not school_name or school_name == "":
        messages["errors"].append("Please provide the School name")

    if not faculty_name or faculty_name == "":
        messages["errors"].append("Please provide the Faculty name")

    # return an error with error messages for failed validations
    if len(messages["errors"]) > 0:

        payload = error_response("Error", {"detail": messages["errors"]})
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

    else:

        try:

            school = School.objects.get(name=school_name)
            faculty = Faculty.objects.get(name=faculty_name)

            departments = Department.objects.filter(
                school=school, faculty=faculty
            )

            serializer = DepartmentSerializer(departments, many=True)

            payload = success_response(
                "Success",
                f"Retrieved all schools in {faculty_name} at {school_name}",
                serializer,
            )
            return Response(data=payload, status=status.HTTP_200_OK)

        except Exception as e:
            payload = error_response("Error", {"details": f"{e}"})
        return Response(
            data=payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
