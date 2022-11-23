from django.urls import path
from . import views

app_name = 'academia'

urlpatterns = [
    
    path('', views.home, name="homepage"),
        
    path('countries', views.CountryList, name="get_countries"),
    
    path('schools', views.SchoolList, name="get_schools"),
    
    path('faculties', views.FacultyList, name="get_faculties"),
    
    path('departments', views.DepartmentList, name="get_departements"),
     
]