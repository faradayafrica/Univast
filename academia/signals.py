# Standard imports
import requests

# Django imports
from django.conf import settings
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save

# Local imports
from .models import School, Country, Faculty, Department, Degree

def webhook(type, fid):

    # Dispatch webhook
    API_URLS = settings.RECIEVER_WEBHOOK_API_URLS
    webhook_urls = API_URLS.split(' ')

    for webhook_url in webhook_urls:
        
        # Include ID in the request body
        payload = {
                    'fid': str(fid),
                    'type': type
                  }
        response_hook = requests.post(webhook_url, data=payload)

def invalidate_country_cache(sender, instance, **kwargs):

    cache_key = f"countries_in_univast"
    if cache.get(cache_key):
        cache.delete(cache_key)

def webhook_clear_school_cache(sender, instance, **kwargs):
    # Clear cache for school
    country_code = instance.country.country_code
    cache_key = f"schools_{country_code}"
    if cache.get(cache_key):
        cache.delete(cache_key)

    # Dispatch webhook
    webhook("school", instance.id)
 
def webhook_clear_faculty_cache(sender, instance, **kwargs):
    school_code = instance.school.code
    cache_key = f"faculties_{school_code}"
    if cache.get(cache_key):
        cache.delete(cache_key)
    
    # Dispatch webhook
    webhook("faculty", instance.id)

def webhook_clear_department_cache(sender, instance, **kwargs):
    # Clear Cache
    school_code = instance.school.code
    faculty_name = instance.faculty.name
    cache_key = f"departments_{school_code}_{faculty_name}"
    if cache.get(cache_key):
        cache.delete(cache_key)
        
    # Dispatch webhook
    webhook("department", instance.id)

post_save.connect(invalidate_country_cache, sender=Country)
post_save.connect(webhook_clear_school_cache, sender=School)
post_save.connect(webhook_clear_faculty_cache, sender=Faculty)
post_save.connect(webhook_clear_department_cache, sender=Department)