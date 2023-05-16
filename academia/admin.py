# Stdlib Imports
from typing import Any, Union

# Django Imports
from django.contrib import admin
from django.http.request import HttpRequest

# Own Imports
from academia.models import (
    Country,
    School,
    Faculty,
    Degree,
    Department,
    Client,
    ClientAPIKey,
)


class AdminCountry(admin.ModelAdmin):
    list_display = (
        "country_code",
        "name",
        "continent",
    )
    search_fields = (
        "continent__icontains",
        "country_code__icontains",
        "name__icontains",
    )
    list_filter = ("continent",)
    empty_value_display = "-empty field-"


class AdminSchool(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "code",
        "type",
        "owned_by",
        "unlisted",
    )
    search_fields = (
        "name__icontains",
        "country__name__icontains",
        "code__icontains",
        "type__icontains",
        "owned_by__icontains",
        "country__country_code__icontains",
        "country__continent__icontains",
    )
    list_filter = ("country", "type", "owned_by", "unlisted")
    empty_value_display = "-empty field-"


class AdminFaculty(admin.ModelAdmin):
    list_display = (
        "name",
        "school",
    )
    search_fields = ["name__icontains", "school__name__icontains"]
    list_filter = ("school",)
    empty_value_display = "-empty field-"
    autocomplete_fields = ["school"]


class AdminDepartment(admin.ModelAdmin):
    list_display = ("name", "duration", "school", "faculty")
    search_fields = (
        "name__icontains",
        "degree__name__icontains",
        "degree__code__icontains",
        "duration__icontains",
        "faculty__name__icontains",
        "school__name__icontains",
        "school__country__name__icontains",
        "school__country__country_code__icontains",
    )
    list_filter = ("degree", "faculty", "duration")
    empty_value_display = "-empty field-"
    autocomplete_fields = ["school", "faculty", "degree"]


class AdminDegree(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name__icontains", "code__icontains")
    list_filter = ("name", "code")
    empty_value_display = "-empty field-"


class AdminClient(admin.ModelAdmin):
    list_display: list = ["id", "name", "email", "is_verified", "client_type"]
    list_filter: list = ["is_verified", "client_type"]


class AdminClientAPIKey(admin.ModelAdmin):
    list_display: list = ["client", "rate", "prefix", "name", "expiry_date"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Union[Any, None] = ...
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Union[Any, None] = ...
    ) -> bool:
        return (
            super().has_delete_permission(request, obj)
            if request.user.is_superuser
            else False
        )
        

admin.site.register(Country, AdminCountry)
admin.site.register(School, AdminSchool)
admin.site.register(Faculty, AdminFaculty)
admin.site.register(Degree, AdminDegree)
admin.site.register(Department, AdminDepartment)
admin.site.register(Client, AdminClient)
admin.site.register(ClientAPIKey, AdminClientAPIKey)
