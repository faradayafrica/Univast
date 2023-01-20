# Stdlib Imports
from typing import List

# Django imports
from django.shortcuts import render
from django.db.models import QuerySet

# Rest Framework Imports
from rest_framework.request import Request
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

# Own imports
from academia.models import Country, School, Faculty, Department
from academia.serializers import (
    CountrySerializer,
    SchoolSerializer,
    FacultySerializer,
    DepartmentSerializer,
)
from academia.selectors import get_country, get_school, get_faculty

# Third Party Imports
from rest_api_payload import success_response


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

        response = success_response(
            status=True,
            message="Retrieved all countries!",
            data=serializer.data,
        )
        return Response(response, status=status.HTTP_200_OK)


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
        \n:type country_name: str
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

        :param school_code: the name of school you wish to get the list of available faculties in.\n
        \n:type school_code: str\n
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


class DepartmentListAPIView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = (HasAPIKey,)
    queryset = Department.objects.prefetch_related("degree").only(
        "id", "name", "degree", "duration"
    )

    def get(
        self, request: Request, school_code: str, faculty_name: str
    ) -> Response:
        """
        This API view retrieves the list of departments in a school.

        :param school_code: the school (code) you wish to get the list of available departments in.
        \n:type school_code: str\n
        \n:param faculty_name: the name of faculty you wish to get the list of available departments in.
        \n:type faculty_name: str\n
        """
        schools = self.get_queryset(school_code, faculty_name)
        serializer = self.serializer_class(
            schools, many=True, context={"request": request}
        )

        response = success_response(
            status=True,
            message=f"Retrieved all departments!",
            data=serializer.data,
        )
        return Response(data=response, status=status.HTTP_200_OK)

    def get_queryset(self, code: str, faculty: str) -> List[QuerySet]:
        school_code = get_school(code)
        faculty_name = get_faculty(faculty)
        return self.queryset.filter(
            school__code=school_code, faculty__name=faculty_name
        )
