# Django imports
from django.contrib import admin
from django.urls import path, include

# Swagger docs
from rest_framework_swagger.views import get_swagger_view

# Swagger docs
schema_view = get_swagger_view(title='Univast API')

from academia import views

urlpatterns = [
    
    path('', views.home, name="homepage"),
     
    path('academia/', include('academia.urls')),
    
    # Admin site
    path('api/auth/admin/', admin.site.urls),
    
    # Documentation by swagger
    path('api/auth/docs/', schema_view, name="documentation"),
]

handler400 = 'academia.views.custom_bad_request_view'
handler403 = 'academia.views.custom_permission_denied_view'
handler404 = 'academia.views.custom_page_not_found_view'
handler500 = 'academia.views.custom_error_view'