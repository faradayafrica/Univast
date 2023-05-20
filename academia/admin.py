# Stdlib Imports
from typing import Any

# Django Imports
from django.contrib import admin
from django.contrib import messages
from django.utils.text import slugify

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
    list_display: list = [
        "name",
        "client",
        "rate",
        "prefix",
        "expiry_date",
    ]

    def save_model(
        self, request: Any, obj: Any, form: Any, change: Any
    ) -> None:
        """
        Override the default save method to manually create client apikey.
        """

        name = form.cleaned_data["name"]
        revoked = form.cleaned_data["revoked"]
        client = form.cleaned_data["client"]
        rate = form.cleaned_data["rate"]
        expires = form.cleaned_data["expiry_date"]

        if not change:
            _, apikey = ClientAPIKey.objects.create_key(
                name=name,
                client=client,
                scope=slugify(name),
                rate=rate,
                expiry_date=expires,
            )

            # show success message to admin user
            messages.success(
                request, f"ApiKey created, kindly copy: {apikey}"
            )

        client_apikey = ClientAPIKey.objects.get(scope=slugify(name))
        client_apikey.revoked = revoked
        client_apikey.name = name
        client_apikey.expiry_date = expires
        client_apikey.client = client
        client_apikey.rate = rate
        client_apikey.save()


admin.site.register(Country, AdminCountry)
admin.site.register(School, AdminSchool)
admin.site.register(Faculty, AdminFaculty)
admin.site.register(Degree, AdminDegree)
admin.site.register(Department, AdminDepartment)
admin.site.register(Client, AdminClient)
admin.site.register(ClientAPIKey, AdminClientAPIKey)
