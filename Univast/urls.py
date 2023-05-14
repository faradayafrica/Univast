# Django imports
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

# Swagger docs
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Own Imports
from Univast.schema_generator import CustomSchemaGenerator


# Swagger docs
schema_view = get_schema_view(
    openapi.Info(
        title="Univast API",
        default_version="1.0",
        description= "An Open Source RESTful Microservice to index all Tertiary Institutions globally. To get started, request for an API Key by contacting us.",
        contact=openapi.Contact(email="engineering@faraday.africa"),
    ),
    public=True,
    generator_class=CustomSchemaGenerator,
)

urlpatterns = [
    path("", include("web.urls")),
    path("academia/", include("academia.urls")),
    # Admin site
    path("api/auth/admin/", admin.site.urls),
    # Documentation by swagger
    path(
        "api/auth/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="api_docs",
    ),
    path(
        "api/auth/redocs/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="api_redocs",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = "academia.views.custom_bad_request_view"
handler403 = "academia.views.custom_permission_denied_view"
handler404 = "academia.views.custom_page_not_found_view"
handler500 = "academia.views.custom_error_view"
