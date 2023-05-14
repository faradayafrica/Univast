# Django Imports
from django.http import HttpRequest

# Rest Framework Imports
from rest_framework.throttling import SimpleRateThrottle


class APIKeyThrottling(SimpleRateThrottle):
    scope = "rate"

    def get_cache_key(self, request: HttpRequest, view):
        api_key = request.headers.get("Authorization").split(" ")[-1]
        return api_key
