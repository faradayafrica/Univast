# Description: This file contains the views for the web app

# Django imports
from django.shortcuts import render

# Local imports
from academia.models import School

# Create your views here.


def get_helpus (request):
    
    schools = School.objects.all().filter(unlisted=True)
    
    return render(request, "soe.html", context={"schools": schools})