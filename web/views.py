# Description: This file contains the views for the web app

# Django imports
from django.shortcuts import render
from django.conf import settings

# Local imports
from academia.models import School

# Create your views here.


def get_helpus (request):
    
    AIRTABLE_API_KEY = settings.AIRTABLE_API_KEY
    AIRTABLE_BASEID = settings.AIRTABLE_BASEID
    AIRTABLE_TABLEID = settings.AIRTABLE_TABLEID
    
    schools = School.objects.all().filter(unlisted=True)
    
    context = {
        'schools': schools,
        'AIRTABLE_API_KEY': AIRTABLE_API_KEY,
        'AIRTABLE_BASEID': AIRTABLE_BASEID,
        'AIRTABLE_TABLEID': AIRTABLE_TABLEID,
    }
    
    return render(request, "soe.html", context)