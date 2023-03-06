# Stdlib Imports
from typing import List

# Django imports
from django.shortcuts import render
from django.core.cache import cache
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
        "ownership",
        "owned_by",
        "founded",
        "address",
    )

    def get(self, request: Request, country_code: str) -> Response:
        """
        This API view retrieves the list of schools.

        :param country_code: the code of country you wish to get the list of available schools in.
        \n:type country_code: str
        """
        # Check if the data is already cached
        key = f"schools_{country_code}"
        data = cache.get(key)

        if data is not None:
            # If data is cached, return it
            
            response = success_response(
                status=True,
                message=f"Retrieved all schools from cache!",
                data=data,
            )
                
            return Response(data=response, status=status.HTTP_200_OK)

        # If data is not cached, fetch it from the queryset
        schools = self.get_queryset(country_code)
        serializer = self.serializer_class(
            schools, many=True, context={"request": request}
        )

        # Cache the data for future requests
        cache.set(key, serializer.data, timeout=None)

        response = success_response(
            status=True,
            message=f"Retrieved all schools from db!",
            data=serializer.data,
        )
        return Response(data=response, status=status.HTTP_200_OK)

    def get_queryset(self, code: str) -> QuerySet[School]:
        country_code = get_country(code)
        return self.queryset.filter(country__country_code=country_code).order_by('name')


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

    def get_queryset(self, code: str) -> QuerySet[Faculty]:
        school_code = get_school(code)
        return self.queryset.filter(school__code=school_code).order_by('name')


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

    def get_queryset(self, code: str, faculty: str) -> QuerySet[Department]:
        school_code = get_school(code)
        faculty_name = get_faculty(faculty)
        return self.queryset.filter(
            school__code=school_code, faculty__name=faculty_name
        ).order_by('name')
