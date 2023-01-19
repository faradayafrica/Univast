# Django Imports
from django.urls import path

# Own Imports
from . import views
from academia.views import (
    CountryListAPIView,
    SchoolListAPIView,
    SchoolFacultyListAPIView,
)

app_name = "academia"

urlpatterns = [
    path("", views.home, name="homepage"),
    path("countries", CountryListAPIView.as_view(), name="get_countries"),
    path("schools", SchoolListAPIView.as_view(), name="get_schools"),
    path(
        "faculties/<str:school_code>/",
        SchoolFacultyListAPIView.as_view(),
        name="get_faculties",
    ),
    path("departments", views.DepartmentList, name="get_departements"),
]
