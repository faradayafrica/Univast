# Django imports
from django.shortcuts import render
from django.core.cache import cache
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

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
from Univast.throttling import APIKeyThrottling
from academia.selectors import get_country, get_school, get_faculty

# Third Party Imports
from rest_api_payload import success_response


# Home page
def home(request):
    return render(request, "academia/index.html", {})


class GetObjectListAPIView(generics.ListAPIView):
    permission_classes = (HasAPIKey,)
    throttle_classes = [APIKeyThrottling]

    def dispatch(self, request, *args, **kwargs):
        self.throttle_classes[0].request = request
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: Request) -> Response:
        """
        This API retrieves an object.
        """

        object_type = request.GET.get("type")
        object_id = request.GET.get("fid")

        if object_type not in ("school", "faculty", "department"):
            response = success_response(
                status=False,
                message="type must either be school, faculty or department",
                data={},
            )
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        if object_type == "school":
            school = get_object_or_404(School, id=object_id)
            serializer = SchoolSerializer(school, many=False)

        elif object_type == "faculty":
            faculty = get_object_or_404(Faculty, id=object_id)
            serializer = FacultySerializer(faculty, many=False)

        elif object_type == "department":
            department = get_object_or_404(Department, id=object_id)
            serializer = DepartmentSerializer(department, many=False)

        response = success_response(
            status=True,
            message="Retrieved updated Fid",
            data=serializer.data,
        )
        return Response(data=response, status=status.HTTP_200_OK)


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
    throttle_classes = [APIKeyThrottling]
    queryset = Country.objects.only("id", "name", "country_code")

    def dispatch(self, request, *args, **kwargs):
        self.throttle_classes[0].request = request
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: Request) -> Response:
        """
        This API retrieves the list of countries (name and code).
        """

        # Check if the data is already cached
        key = "countries_in_univast"
        data = cache.get(key)

        if data is not None:
            response = success_response(
                status=True,
                message="Retrieved all schools from cache!",
                data=data,
            )

            return Response(data=response, status=status.HTTP_200_OK)

        countries = self.get_queryset()
        serializer = self.serializer_class(countries, many=True)

        # Cache the data for future requests
        cache.set(key, serializer.data, timeout=None)

        response = success_response(
            status=True,
            message="Retrieved all countries from db!",
            data=serializer.data,
        )
        return Response(response, status=status.HTTP_200_OK)


class SchoolListAPIView(generics.ListAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (HasAPIKey,)
    throttle_classes = [APIKeyThrottling]
    throttle_scope = "rate"
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
    ).filter(unlisted=False)

    def dispatch(self, request, *args, **kwargs):
        self.throttle_classes[0].request = request
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: Request, country_id: str) -> Response:
        """
        This API view retrieves the list of schools.

        :param country_id: the code of country you wish to
            get the list of available schools in.
        \n:type country_id: str
        """
        # Check if the data is already cached
        key = f"schools_{country_id}"
        data = cache.get(key)

        if data is not None:
            response = success_response(
                status=True,
                message="Retrieved all schools from cache!",
                data=data,
            )

            return Response(data=response, status=status.HTTP_200_OK)

        # If data is not cached, fetch it from the queryset
        schools = self.get_queryset(country_id)
        serializer = self.serializer_class(
            schools, many=True, context={"request": request}
        )

        # Cache the data for future requests
        cache.set(key, serializer.data, timeout=None)

        response = success_response(
            status=True,
            message="Retrieved all schools from db!",
            data=serializer.data,
        )
        return Response(data=response, status=status.HTTP_200_OK)

    def get_queryset(self, country_id: str) -> QuerySet[School]:
        country_code = get_country(country_id)
        return self.queryset.filter(
            country_id=country_id
        ).order_by("name")


class SchoolFacultyListAPIView(generics.ListAPIView):
    serializer_class = FacultySerializer
    permission_classes = (HasAPIKey,)
    throttle_classes = [APIKeyThrottling]
    queryset = Faculty.objects.only("id", "name")

    def dispatch(self, request, *args, **kwargs):
        self.throttle_classes[0].request = request
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: Request, school_id: str) -> Response:
        """
        This API view retrieves the list of faculties in a school.

        :param school_id: the id of school you wish to
            get the list of available faculties in.\n
        \n:type school_id: str\n
        """

        # Check if the data is already cached
        key = f"faculties_{school_id}"
        data = cache.get(key)

        if data is not None:
            response = success_response(
                status=True,
                message="Retrieved all faculties from cache!",
                data=data,
            )

            return Response(data=response, status=status.HTTP_200_OK)

        faculties = self.get_queryset(school_id)
        serializer = self.serializer_class(
            faculties, many=True, context={"request": request}
        )

        # Cache the data for future requests
        cache.set(key, serializer.data, timeout=None)

        response = success_response(
            status=True,
            message="Retrieved all faculties from db!",
            data=serializer.data,
        )
        return Response(data=response, status=status.HTTP_200_OK)

    def get_queryset(self, school_id: str) -> QuerySet[Faculty]:
        school_code = get_school(school_id)
        return self.queryset.filter(school_id=school_id).order_by("name")


class DepartmentListAPIView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = (HasAPIKey,)
    throttle_classes = [APIKeyThrottling]
    queryset = Department.objects.prefetch_related("degree").only(
        "id", "name", "degree", "duration"
    )

    def dispatch(self, request, *args, **kwargs):
        self.throttle_classes[0].request = request
        return super().dispatch(request, *args, **kwargs)

    def get(
        self, request: Request, school_id: str, faculty_id: str
    ) -> Response:
        """
        This API view retrieves the list of departments in a school.

        :param school_id: the school (id) you wish to
            get the list of available departments in.
        \n:type school_id: str\n
        \n:param faculty_id: the id of faculty you wish
            to get the list of available departments in.
        \n:type faculty_id: str\n
        """

        # Check if the data is already cached
        key = f"departments_{school_id}_{faculty_id}"
        data = cache.get(key)

        if data is not None:
            response = success_response(
                status=True,
                message="Retrieved all departments from cache!",
                data=data,
            )

            return Response(data=response, status=status.HTTP_200_OK)

        schools = self.get_queryset(school_id, faculty_id)
        serializer = self.serializer_class(
            schools, many=True, context={"request": request}
        )

        # Cache the data for future requests
        cache.set(key, serializer.data, timeout=None)

        response = success_response(
            status=True,
            message="Retrieved all departments from db!",
            data=serializer.data,
        )
        return Response(data=response, status=status.HTTP_200_OK)

    def get_queryset(self, school_id: str, faculty_id: str) -> QuerySet[Department]:
        school_code = get_school(school_id)
        faculty_name = get_faculty(faculty_id)
        return self.queryset.filter(
            school_id=school_id, faculty_id=faculty_id
        ).order_by("name")
