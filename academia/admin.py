# Stdlib Imports
from typing import Any

# Django Imports
from django.contrib import admin
from django.contrib import messages
from django.utils.text import slugify

# Own Imports
from academia.models import (
    Client,
    Degree,
    School,
    Course,
    Faculty,
    Country,
    Semester,
    Programme,
    Department,
    ClientAPIKey,
    AcademicSession,
    AcademicCalendar,
    LectureTimetable,
)

from academia.forms import AcademicCalendarForm
    
class AdminProgramme(admin.ModelAdmin):
    list_display = [
        "name",
        "school",
        "duration",
        "degree_type"
    ]
    search_fields = ["name__icontains", "school__name__icontains", "parent_programme__name__icontains", "school__country__name__icontains", "school__country__country_code__icontains", "parent_programme__school__name__icontains"]
    list_filter = ("school", "duration")
    empty_value_display = "-empty field-"
    autocomplete_fields = ["school", "parent_programme"]


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


class AdminAcademicSession(admin.ModelAdmin):
    list_display = [
        "school",
        "programme",
        "start_date",
        "end_date",
        "is_current_session"
    ]
    search_fields = ("name__icontains", "school__name__icontains", "school__country__name__icontains", "school__country__country_code__icontains")
    empty_value_display = "-empty field-"
    autocomplete_fields = ["school", "programme"]


class AcademicCalendarAdmin(admin.ModelAdmin):
    form = AcademicCalendarForm
    search_fields = [
        "academic_session__name__icontains",
        "academic_session__school__name__icontains",
        "academic_session__school__country__name__icontains",
        "academic_session__school__country__country_code__icontains",
        
        "school__name__icontains",
        "school__country__name__icontains",
        "school__country__country_code__icontains",
        
        "semester__name__icontains"
    ]


class AdminSemester(admin.ModelAdmin):
    list_display = ("name", "academic_session", "start_date", "end_date", "is_current_semester")
    search_fields = [
        "name__icontains",
        "academic_session__name__icontains",
        "academic_session__school__name__icontains",
        "academic_session__school__country__name__icontains",
        "academic_session__school__country__country_code__icontains",
    ]
    list_filter = ("academic_session", "is_current_semester")
    empty_value_display = "-empty field-"
    autocomplete_fields = ["school", "academic_session"]


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
    search_fields = ["name__icontains", "school__name__icontains", "school__code__icontains", "programme__name__icontains", "programme__school__name__icontains"]
    list_filter = ("school", "programme")
    empty_value_display = "-empty field-"
    autocomplete_fields = ["school", "programme"]


class AdminDepartment(admin.ModelAdmin):
    list_display = ("name", "duration", "school", "faculty")
    search_fields = (
        "name__icontains",
        "degree__name__icontains",
        "degree__code__icontains",
        "duration__icontains",
        "faculty__name__icontains",
        "school__name__icontains",
        "school__code__icontains",
        "school__country__name__icontains",
        "school__country__country_code__icontains",
    )
    list_filter = ("degree", "faculty", "duration")
    empty_value_display = "-empty field-"
    autocomplete_fields = ["school", "faculty", "degree"]


class LectureTimetableAdmin(admin.ModelAdmin):
    list_display = ("department", "academic_session", "semester", "level")
    empty_value_display = "-empty field-"
    search_fields = [
        "department__name__icontains", 
        "academic_session__name__icontains",
        "programme_school__name__contains",
        "programme__school__code__contains",
        "academic_session__school__name__icontains", 
        "academic_session__school__code__icontains", 
        "semester__name__icontains", 
        "level__icontains"
    ]
    list_filter = ("department", "academic_session", "semester", "level")
    autocomplete_fields = ["department", "academic_session", "semester"]
    
class AdminCourse(admin.ModelAdmin):
    list_display = ("school", "name", "code")
    empty_value_display = "-empty field-"
    search_fields = ["name__icontains", "school__name__icontains", "school__code__icontains"]
    list_filter = ("school", "code")
    autocomplete_fields = ["school"]

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


admin.site.register(School, AdminSchool)
admin.site.register(Client, AdminClient)
admin.site.register(Degree, AdminDegree)
admin.site.register(Course, AdminCourse)
admin.site.register(Faculty, AdminFaculty)
admin.site.register(Country, AdminCountry)
admin.site.register(Semester, AdminSemester)
admin.site.register(Programme, AdminProgramme)
admin.site.register(Department, AdminDepartment)
admin.site.register(ClientAPIKey, AdminClientAPIKey)
admin.site.register(AcademicSession, AdminAcademicSession)
admin.site.register(AcademicCalendar, AcademicCalendarAdmin)
admin.site.register(LectureTimetable, LectureTimetableAdmin)
