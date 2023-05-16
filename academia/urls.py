# Django Imports
from django.urls import path

# Own Imports
from academia.views import (
    home,
    SchoolListAPIView,
    CountryListAPIView,
    GetObjectListAPIView,
    DepartmentListAPIView,
    SchoolFacultyListAPIView,
)

app_name = "academia"

urlpatterns = [
    path("", home, name="homepage"),
    path("fetch", GetObjectListAPIView.as_view(), name="get_object"),
    path("countries", CountryListAPIView.as_view(), name="get_countries"),
    path(
        "schools/<str:country_code>",
        SchoolListAPIView.as_view(),
        name="get_schools",
    ),
    path(
        "faculties/<str:school_code>",
        SchoolFacultyListAPIView.as_view(),
        name="get_faculties",
    ),
    path(
        "departments/<str:school_code>/<str:faculty_name>",
        DepartmentListAPIView.as_view(),
        name="get_departments",
    ),
]
