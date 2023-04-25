# Django Imports
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Own Imports
from . import views

# local imports
from academia.views import home

app_name = "academia"

urlpatterns = [
    path("", home, name="homepage"),
    path("helpus", views.get_helpus, name="helpus"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)