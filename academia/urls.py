# Django Imports
from django.urls import path

# Own Imports
from . import views
from academia.views import (
    CountryListAPIView,
    SchoolListAPIView,
    SchoolFacultyListAPIView,
    DepartmentListAPIView,
)

app_name = "academia"

urlpatterns = [
    path("", views.home, name="homepage"),
    path("countries", CountryListAPIView.as_view(), name="get_countries"),
    path("schools/<str:country_code>", SchoolListAPIView.as_view(), name="get_schools"),
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
