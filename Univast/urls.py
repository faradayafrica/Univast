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
