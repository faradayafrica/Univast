# Django imports
from django.core.cache import cache
from django.db.models.signals import post_save

# Local imports
from academia.models import School, Country, Faculty, Department
from academia.tasks import dispatch_webhook


def invalidate_country_cache(sender, instance, **kwargs):

    cache_key = f"countries_in_univast"
    if cache.get(cache_key):
        cache.delete(cache_key)

def webhook_clear_school_cache(sender, instance, **kwargs):
    # Clear cache for school
    country_id = instance.country.id
    cache_key = f"schools_{country_id}"
    if cache.get(cache_key):
        cache.delete(cache_key)

    # Dispatch webhook
    dispatch_webhook.delay("school", instance.id)
 
def webhook_clear_faculty_cache(sender, instance, **kwargs):
    school_id = instance.school.id
    cache_key = f"faculties_{school_id}"
    if cache.get(cache_key):
        cache.delete(cache_key)
    
    # Dispatch webhook
    dispatch_webhook.delay("faculty", instance.id)

def webhook_clear_department_cache(sender, instance, **kwargs):
    # Clear Cache
    school_id = instance.school.id
    faculty_id = instance.faculty.id
    cache_key = f"departments_{school_id}_{faculty_id}"
    if cache.get(cache_key):
        cache.delete(cache_key)
        
    # Dispatch webhook
    dispatch_webhook.delay("department", instance.id)

post_save.connect(invalidate_country_cache, sender=Country)
post_save.connect(webhook_clear_school_cache, sender=School)
post_save.connect(webhook_clear_faculty_cache, sender=Faculty)
post_save.connect(webhook_clear_department_cache, sender=Department)