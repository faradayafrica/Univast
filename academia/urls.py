# Django Imports
from django.urls import path

# Own Imports
from . import views
from academia.views import CountryListAPIView

app_name = "academia"

urlpatterns = [
    path("", views.home, name="homepage"),
    path("countries", CountryListAPIView.as_view(), name="get_countries"),
    path("schools", views.SchoolList, name="get_schools"),
    path("faculties", views.FacultyList, name="get_faculties"),
    path("departments", views.DepartmentList, name="get_departements"),
]
