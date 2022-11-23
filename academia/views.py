# Django imports
from django.shortcuts import render

# Rest Framework Imports
from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import filters, views, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

# Own imports
from .models import (
    Country,
    School,
    Faculty,
    Department
)

from .serializers import (
    CountrySerializer,
    SchoolSerializer,
    FacultySerializer,
    DepartmentSerializer,
)

from .utills import (
    SuccessResponse,
    ErrorResponse
)

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

# Fetches All Countries
@api_view(['GET'])
@permission_classes((AllowAny,))
def CountryList(request):
    try:
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        
        payload = SuccessResponse("Success", "Retrieved all countries", serializer)
        return Response(data=payload, status=status.HTTP_200_OK)
        
    except Exception as e:
        
        payload = ErrorResponse("Error", {'details': f"{e}"})
        return Response(data=payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Fetch Schools in a Country
@api_view(['GET'])
@permission_classes((AllowAny,))
def SchoolList(request):
    
    # initialize empty array to hold error message(s)
    messages = {'errors': []}
    
    
    # get required parameters
    country_name = request.data.get('country')
        
    # perform validations for required parameters
    if not country_name or country_name == "":
        messages['errors'].append('Please provide the country name')

    # return an error with error messages for failed validations
    if len(messages['errors']) > 0:
    
        payload = ErrorResponse("Error", {"detail": messages['errors']})
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        
        try:
            
            country = Country.objects.get(name=country_name)
            
            schools = School.objects.filter(country=country)
            
            serializer = SchoolSerializer(schools, many=True)
            
            payload = SuccessResponse("Success", f"Retrieved all schools in {country_name}", serializer)
            return Response(data=payload, status=status.HTTP_200_OK)

        except Exception as e:
            payload = ErrorResponse("Error", {'details': f"{e}"})
        return Response(data=payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Fetch all Faculties in a School
@api_view(['GET'])
@permission_classes((AllowAny,))
def FacultyList(request):
    # initialize empty array to hold error message(s)
    messages = {'errors': []}
    
    
    # get required parameters
    school_name = request.data.get('school')
        
    # perform validations for required parameters
    if not school_name or school_name == "":
        messages['errors'].append('Please provide the School name')

    # return an error with error messages for failed validations
    if len(messages['errors']) > 0:
    
        payload = ErrorResponse("Error", {"detail": messages['errors']})
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        
        try:
            
            school = School.objects.get(name=school_name)
            
            faculties = Faculty.objects.filter(school=school)
            
            serializer = FacultySerializer(faculties, many=True)
            
            payload = SuccessResponse("Success", f"Retrieved all schools in {school_name}", serializer)
            return Response(data=payload, status=status.HTTP_200_OK)

        except Exception as e:
            payload = ErrorResponse("Error", {'details': f"{e}"})
        return Response(data=payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Fetch all Departments in a Faculty.
@api_view(['GET'])
@permission_classes((AllowAny,))
def DepartmentList(request):
    # initialize empty array to hold error message(s)
    messages = {'errors': []}
    
    
    # get required parameters
    school_name = request.data.get('school')
    faculty_name = request.data.get('faculty')
        
    # perform validations for required parameters
    if not school_name or school_name == "":
        messages['errors'].append('Please provide the School name')
        
    if not faculty_name or faculty_name == "":
        messages['errors'].append('Please provide the Faculty name')

    # return an error with error messages for failed validations
    if len(messages['errors']) > 0:
    
        payload = ErrorResponse("Error", {"detail": messages['errors']})
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        
        try:
            
            school = School.objects.get(name=school_name)
            faculty = Faculty.objects.get(name=faculty_name)
            
            departments = Department.objects.filter(school=school, faculty=faculty)
            
            serializer = DepartmentSerializer(departments, many=True)
            
            payload = SuccessResponse("Success", f"Retrieved all schools in {faculty_name} at {school_name}", serializer)
            return Response(data=payload, status=status.HTTP_200_OK)

        except Exception as e:
            payload = ErrorResponse("Error", {'details': f"{e}"})
        return Response(data=payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
