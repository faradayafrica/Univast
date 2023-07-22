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
        "schools/<str:country_id>",
        SchoolListAPIView.as_view(),
        name="get_schools",
    ),
    path(
        "faculties/<str:school_id>",
        SchoolFacultyListAPIView.as_view(),
        name="get_faculties",
    ),
    path(
        "departments/<str:school_id>/<str:faculty_id>",
        DepartmentListAPIView.as_view(),
        name="get_departments",
    ),
    path('clear-cache/', views.clear_and_reset_cache, name='clear_cache'),
]
