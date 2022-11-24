# REST framework imports
from rest_framework import serializers
from django.http import JsonResponse

# Own imports
from .models import (
    Country,
    School,
    Faculty,
    Degree,
    Department
)

class DegreeSerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the Faculty database model
    
    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """
    class Meta:
        model = Degree
        fields = [
            'name',
            ]   
        # fields = '__all__'  

class CountrySerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the Country database model
    
    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """
    class Meta:
        model = Country
        fields = [
            'name',
            'country_code',
            ]    
        
class SchoolSerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the School database model
    
    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """
    
    logo = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = School
        fields = [
            'type',
            'name',
            'code',
            'website',
            'logo',
            'ownership',
            'owned_by',
            ]
        
    def get_logo(self, obj):
        request = self.context.get("request")
        logo = request.scheme + '://' + request.META['HTTP_HOST'] + '/images/' + str(obj.logo)
        return logo

class FacultySerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the Faculty database model
    
    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """
    class Meta:
        model = Faculty
        fields = [
            'name',
            ]

class DepartmentSerializer(serializers.ModelSerializer):
    """
    This seriliazer serilizes data for the Department database model
    
    :param: Request and/or object
    :return: Serilized data specified by provided fields
    """
    
    degree = DegreeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Department
        fields = [
            'name',
            'degree',
            'duration'
            ]