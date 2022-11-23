from django.contrib import admin
from .models import (
    Country,
    School,
    Faculty,
    Degree,
    Department
)

class AdminCountry(admin.ModelAdmin):
    list_display = ('country_code', 'name', 'continent',)
    search_fields = ('continent', 'country_code', 'name')
    list_filter = ('continent',)
    empty_value_display = '-empty field-'

class AdminSchool(admin.ModelAdmin):
    list_display = ('listed', 'type', 'name', 'code') 
    search_fields = ('name', 'country',)
    list_filter = ('country', 'type', 'listed')
    empty_value_display = '-empty field-'

class AdminFaculty(admin.ModelAdmin):
    list_display = ('name', 'school')
    search_fields = ('continent', 'country_code', 'name')
    list_filter = ('school',)
    empty_value_display = '-empty field-'
    
class AdminDepartment(admin.ModelAdmin):
    list_display = ('faculty', 'name', 'duration')
    search_fields = ('name', 'degree', 'duration')
    list_filter = ('degree', 'faculty', 'duration')
    empty_value_display = '-empty field-'

class AdminDegree(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    list_filter = ('name', 'code')
    empty_value_display = '-empty field-'


admin.site.register(Country, AdminCountry)
admin.site.register(School, AdminSchool)
admin.site.register(Faculty, AdminFaculty)
admin.site.register(Degree, AdminDegree)
admin.site.register(Department, AdminDepartment)
