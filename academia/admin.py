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
    list_display = ('name', 'code', 'type', 'owned_by', 'listed',) 
    search_fields = ('name', 'country',)
    list_filter = ('country', 'type', 'owned_by', 'listed')
    empty_value_display = '-empty field-'

class AdminFaculty(admin.ModelAdmin):
    list_display = ('name', 'school')
    search_fields = ('continent', 'country_code', 'name')
    list_filter = ('school',)
    empty_value_display = '-empty field-'
    autocomplete_fields = ['school']
    
class AdminDepartment(admin.ModelAdmin):
    list_display = ('faculty', 'name', 'duration')
    search_fields = ('name', 'degree', 'duration')
    list_filter = ('degree', 'faculty', 'duration')
    empty_value_display = '-empty field-'
    autocomplete_fields = ['faculty', 'school']

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
