from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import School

def clear_school_cache(sender, instance, **kwargs):
    print("Clearing cache")
    country_code = instance.country.country_code
    print(country_code)
    cache.delete(f"schools_{country_code}")
    print("Cache cleared")
    
post_save.connect(clear_school_cache, sender=School)